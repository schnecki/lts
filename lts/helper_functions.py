from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Costs
from django import forms
from operator import itemgetter, attrgetter, methodcaller
from functools import cmp_to_key, reduce

########## Functions / Procedures

def sort_order_list_key(x):
    "Function which defines the order for the list of orders."

    return (not x.is_rush_order(),x.release_date,x.order_id)

def sort_order_list_order_book(x):
    "Function which defines the order for the list of orders."

    return (x.due,x.order_id)

def sort_order_order_book(orders):
    "This functions sorts the given orders by a) due date and b) order_id."

    sorted_orders = sorted(orders,key=sort_order_list_order_book)
    return list(sorted_orders)


def sort_order_list(orders):
    "This functions sorts the given orders by a) Rush-order b) release date and c) order_id."

    sorted_orders = sorted(orders,key=sort_order_list_key)
    return list(sorted_orders)


def get_releasable_orders(page, set_order_nr=False):
    "This function returns a sorted list of releasable orders."
    all_orders = get_all_orders(page)
    current_period = page.player.period

    releasable_orders = filter(lambda o: o.release_date is None and \
                               o.arrival <= current_period.start, all_orders)
    sorted_orders = sort_order_order_book(releasable_orders)
    if set_order_nr:
        lst = list(map(lambda x: x.nr, filter(lambda x: x.nr is not None, all_orders)))
        lst.append(0)
        order_nr = max(lst)

        sorted_orders_2 = []
        for o in sorted_orders:
            if o.nr is None:
                order_nr = order_nr + 1
                o.nr = order_nr
                o.save()
            sorted_orders_2.append(o)

        return sorted_orders_2
    return sorted_orders

def is_test_phase(page):
    return page.player.test_round


def get_released_orders(page):
    "This function returns the sorted released orders."
    all_orders = get_all_orders(page)
    return sort_order_list(filter(lambda o: o.release_date is not None, all_orders))

def get_all_orders(page):
    test_phase = is_test_phase(page)
    all_orders = page.player.particip.orders.all()
    return list(filter(lambda o: o.from_test_round == test_phase, all_orders))


def get_finished_orders(page):
    "This function returns all finished orders."

    all_orders = get_all_orders(page)
    return list(filter(lambda o: o.sent_date is not None, all_orders))

def get_processing_orders(page):
    "This function returns a list of all orders which are being processed right now."

    all_orders = get_all_orders(page)
    return list(filter(lambda o: o.is_processing, all_orders))


def get_fgi_orders(page):
    "This function returns all orders in the fgi."

    all_orders = get_all_orders(page)
    return list(filter(lambda o:
                       o.sent_date is None and
                       o.fgi_arrived_date is not None, all_orders))

def get_test_round_drop_nr(page):
    test_round_len = abs(Constants.test_round_ID)
    return int((page.player.subsession.round_number-1) / test_round_len)*test_round_len


def get_last_known_flow_time(page):

    test_phase = is_test_phase(page)
    flow_time_list = [p.flow_time for p in page.player.in_previous_rounds()
                      if test_phase or not p.test_round]
    if test_phase:
        # drop all from other trial rounds
        nr = get_test_round_drop_nr(page)
        flow_time_list = flow_time_list[nr:]

    flow_time_list.reverse()
    flow_time_list.append(page.player.subsession.session.config['start_flow_time'])
    # print("Flow_Time_List: ", flow_time_list)
    flow_time_list = list(filter(lambda x: x > 0, flow_time_list))
    # print(flow_time_list)
    return flow_time_list[0]

def get_sum_costs(page):

    test_phase = is_test_phase(page)
    cost_elems = [p.costs for p in page.player.in_previous_rounds()
                  if test_phase or not p.test_round ]
    if test_phase:
        # drop all from other trial rounds
        nr = get_test_round_drop_nr(page)
        # print("nr: " , nr)
        # print("cost_elems before: " , cost_elems)
        cost_elems = cost_elems[nr:]

    cost_elems.append(page.player.costs) # add current costs object to list

    # print("cost_elems: ", cost_elems)

    wip = sum(map(lambda x: x.wip,cost_elems))
    fgi = sum(map(lambda x: x.fgi,cost_elems))
    bo = sum(map(lambda x: x.bo,cost_elems))
    return Costs(wip=wip, fgi=fgi, bo=bo)


def process_order(page, order, sim_time_left):
    "This function processes an order to either the finished product, or the end of \
    the period."

    order_time_left = order.time_until_finished

    if sim_time_left <= 0:
        return 0

    if sim_time_left >= order_time_left: # order will be finished processing
        order.time_until_finished = 0
        order.is_processing = False
        sim_time_left = sim_time_left - order_time_left
        order.fgi_arrived_date = page.player.period.end + 1 - sim_time_left
        # order.save()
        # print("order: ", order)
        # print("p end: ", page.player.period.end)
        # print("sim_time_left: ", sim_time_left)
        return sim_time_left
    else:                       # order cannot be finished processing
        order.time_until_finished -= sim_time_left
        order.is_processing = True
        # order.save()
        return 0                # ... sim_time_left = 0

def simulate(page):
    "This function simulations the production system. It first finishes the processing\
    orders and then fills the machine and processes until the end of the period. It \
    expects that at most only one order can be in processing state. That is it expects \
    a single-machine single-stage production system. Orders are shipped at the end of \
    the period, if done processing and due (no early deliveries!)."

    sim_start = page.player.period.start
    sim_end = page.player.period.end
    sim_time_left = abs(sim_end-sim_start)+1 # no positive and negative combination
                                             # of numbers allowed!


    # print("Period: ", sim_start, sim_end)

    all_orders = get_all_orders(page)

    processing_orders = list(filter(lambda o: o.is_processing and \
                                    o.fgi_arrived_date is None, all_orders))
    released_orders = get_released_orders(page)

    # Process order which may still be in the machine
    if processing_orders:
        sim_time_left = process_order(page, processing_orders[0], sim_time_left)


    # Process released orders one after the other
    for o in released_orders:
        if sim_time_left <= 0:
            break               # Stop loop
        if (o.time_until_finished > 0):
            sim_time_left = process_order(page, o, sim_time_left)

    # Ship orders
    to_ship = [o for o in all_orders if
               o.due <= sim_end and               # is due
               o.fgi_arrived_date is not None and # is in inventory (production
                                                  # finished)
               o.sent_date is None]               # is not yet shipped

    for o in to_ship:
        o.sent_date = sim_end

    # save all back-orders before processing (as their state will be modified, but
    # still back-order costs have to be paid for the lateness)
    orders_bo = [o for o in all_orders if
                 o.sent_date is None and
                 o.due <= sim_end]

    # Add costs
    orders_wip = [o for o in all_orders if
                  o.release_date is not None and # released
                  o.fgi_arrived_date is None]    # not yet finished production
    orders_fgi = [o for o in all_orders if
                  o.fgi_arrived_date is not None and # finished production
                  o.sent_date is None]               # not yet send

    csts_wip = len(orders_wip) * models.Constants.costs_wip # in
    csts_fgi = len(orders_fgi) * models.Constants.costs_fgi # costs are defined
    csts_bo = len(orders_bo) * models.Constants.costs_bo    # models.Constant

    page.player.costs.wip = csts_wip
    page.player.costs.fgi = csts_fgi
    page.player.costs.bo = csts_bo
    page.player.costs.save()    # save costs to db
    page.player.payoff = csts_wip + csts_fgi + csts_bo # save as payoff for output

    # calculate statistics
    # print("all: ", list(all_orders))
    orders_finished_this_period = [o for o in all_orders if
                                   o.fgi_arrived_date is not None and
                                   o.fgi_arrived_date > sim_start and
                                   o.fgi_arrived_date <= (sim_end+1)]
    # print("fin: " , orders_finished_this_period)


    orders_flow_times = list(map(lambda o: o.fgi_arrived_date-o.release_date,
                                 orders_finished_this_period))
    if len(orders_flow_times) == 0:
        page.player.flow_time = get_last_known_flow_time(page)
    else:
        # print("flow_time:", orders_flow_times)
        page.player.flow_time = sum(orders_flow_times)/len(orders_flow_times)

    # increase current period counter
    page.player.particip.in_current_period += 1
    page.player.particip.save()

    # Ensure new states are written to db
    for o in all_orders:
        o.save()


