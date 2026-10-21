## Decode
[b1] More customers lead to more referrals, and more referrals lead to more customers. This closed loop is reinforcing (it amplifies itself) and continues growing indefinitely, with no stated limit.
[b2] The room temperature is compared with a target. If it is below the target, the heater turns on and warms the room. When the target is reached, the heater turns off. This is a balancing loop that settles at the target (the goal).
[b3] The tank level is a stock (an amount that accumulates). The inlet is the inflow and the drain is the outflow. When inflow exceeds outflow, the level rises; otherwise it falls.
[b4] When inventory is below the target, an order is placed. Deliveries arrive only after a 2-week delay, so people over-order. As a result, inventory swings (oscillates) around the target. This is a balancing relationship with a delay (overshoot/oscillation).
[b5] Four steps in sequence: collect data; once done, clean it; once done, analyze it; once done, publish the results.
[b6] Check each request (every request is checked). If it is valid, process it; otherwise reject it and then tell the sender (the rejection happens first, then the sender is told).
[b7] An order splits into two parallel tasks, packing and billing. When both are done, the order ships.
[b8] Reinforcing loop: more births lead to a larger population, which leads to more births (grows). Balancing loop: a larger population means fewer rations (per capita), fewer rations means more deaths, and more deaths mean a smaller population. This second loop is balancing and settles at the capacity (the goal).
[b9] Try the job. If it fails, wait, then retry (in that order). After 3 failures, escalate to human review.
[b10] A factory is a system containing three subsystems: intake, assembly and inspection. Parts flow from suppliers to intake, then to assembly, then to inspection. Finished goods flow from inspection to customers. Defects flow back from inspection to assembly (a rework loop).
## Encode
[h1] stress cut sleep cut stress, grows.
[h2] balance stock, deposits in, withdrawals out, fees out; each month: interest in; balance lift interest lift balance, grows.
[h3] message to queue; queue full: drop message; else worker picks up, processes, writes result to storage.
[h4] demand over supply: prices rise; prices cut demand lift prices, seeks equilibrium; prices lift supply lag cut prices, seeks equilibrium.
DIFFICULTY: 4 and the hardest part is knowing how to express loops that mix ordinary content words with lift/cut chains (for example where to place lag, how to say a proportional or conditional flow, and when a chain counts as closed), since the spec gives few examples.
