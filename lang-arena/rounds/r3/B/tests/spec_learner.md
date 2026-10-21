## Decode
[b1] Customers raise referrals, and referrals raise customers in turn: more customers bring more referrals, which bring still more customers. This is a reinforcing (runaway) loop that escalates without end ("forever").
[b2] The room is compared with the target. When the room is below target, the heater turns on and warms the room. When the target is reached, the heater turns off. The loop is balancing: it pulls the room toward the target and settles there. The spec gives no explicit cause chain here, so the loop type comes from the marker alone.
[b3] Tank level is a stock: it accumulates, rising while the inlet's inflow exceeds the drain's outflow and falling while the drain's outflow exceeds the inlet's inflow. The inlet adds to the tank level; the drain drains it.
[b4] When inventory falls below target, an order is placed. The ordering acts 2 weeks late (lag), so the result is over-ordering. The effect swings (oscillates). The spec does not say what quantity the swing applies to, and there is no explicit loop marker.
[b5] Four steps in sequence: collect data, then clean it, then analyze it, then publish the results. Each step starts only after the previous one finishes.
[b6] Check requests first. If a request is valid, process it. Otherwise, reject it and then tell the sender. The reject and tell-sender steps belong only to the invalid case.
[b7] Packing and billing run at the same time (parallel). Ship happens only after both are done (join, waiting for all). The sentence does not say whether "order" is a thing (an order) or an action (to order); the packing, billing and shipping steps are clear either way.
[b8] Two loops. (1) Runaway: births raise population, and population raises births, so growth escalates. (2) Balancing at capacity: population lowers rations, rations lower deaths, and deaths lower population. This loop pulls population toward capacity and settles there. Capacity is the named limit.
[b9] Try the job. If it fails, wait, then retry. After three failures (a count threshold), human review. The spec does not say whether retrying continues after the third failure.
[b10] Parts flow from suppliers to the factory. The factory is a system with three subsystems in order: intake, assembly, inspection. Parts enter at intake and leave from inspection, then flow to customers. Defects flow back to assembly (rework). The spec does not say where defects originate.

## Encode
[h1] stress lowers sleep lowers stress, runaway
[h2] account balance stock, deposits inflow, withdrawals outflow, fees outflow; each month: account balance raises interest, interest inflow
[h3] message to queue; queue full: drop message, else worker picks up message, processes it, writes result to storage
[h4] demand exceeds supply: price rises; price lowers demand raises price, balancing at equilibrium; price raises supply lag lowers price, balancing at equilibrium

DIFFICULTY: 6 The hardest part is encoding conditions the spec has no keyword for, such as "exceeds" and "in proportion", which I had to fold into raises, and the sentences whose loops or subjects are left implicit, such as b2 and b7.
