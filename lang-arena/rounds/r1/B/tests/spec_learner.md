## Decode
[b1] More customers cause more referrals, and more referrals cause more customers. This is a closed reinforcing loop (self-amplifying) that continues to grow forever (no limit stated).
[b2] Room temperature is compared with a target. When the room is below target, the heater turns on and warms the room. When the target is reached, the heater turns off. This is a balancing loop that pulls the room toward the target and settles there.
[b3] Tank level is a stock (an amount that accumulates). The inlet is an inflow into the stock; the drain is an outflow. When inflow exceeds outflow, the level rises; otherwise it falls.
[b4] When inventory is below target, an order is placed. Deliveries arrive only after a delay of 2 weeks (lag), so the ordering over-orders in the meantime. As a result, inventory oscillates (swings) around the target (a balancing loop with delay).
[b5] Four steps in strict sequence: collect data; after that finishes, clean it; after that finishes, analyze it; after that finishes, publish the results.
[b6] Check each request. If it is valid, process it; otherwise reject it and tell the sender.
[b7] An order splits into two parallel tasks that run at once: packing and billing. Only when both are done, ship the order.
[b8] More births cause a larger population, and a larger population causes more births: a reinforcing loop that grows. Also, a larger population causes fewer rations (reduces rations); more rations cause fewer deaths; more deaths cause a smaller population: a closed loop (balancing) that seeks capacity, i.e. population settles toward the carrying capacity.
[b9] Try a job. If it fails, wait and then retry. If it has failed 3 times, stop retrying and send it to human review.
[b10] A factory has three subsystems: intake, assembly and inspection. Parts flow from suppliers to intake to assembly to inspection; finished goods flow to customers; defects flow back to assembly (a rework loop).
## Encode
[h1] stress cut sleep cut stress, grows.
[h2] balance stock, deposits in, withdrawals out, fees out; each month: interest in; balance lift interest lift balance, grows.
[h3] message to queue; queue full: drop, else worker picks up then processes then writes result to storage.
[h4] demand vs supply; demand over supply: prices rise; prices cut demand lift prices, seeks equilibrium; prices lift supply lag delay cut prices, seeks equilibrium.
DIFFICULTY: 4 and the hardest part was deciding how to express loops with mixed lift/cut signs, delays, and conditions (like "over", "each month", "full") that the spec leaves to ordinary words or semicolon clauses.
