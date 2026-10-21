[b1] A reinforcing (positive feedback) loop: more customers lead to more referrals, and more referrals bring in more customers. Nothing limits it, so growth is unbounded and keeps accelerating.

[b2] A thermostat-style negative feedback (balancing) loop. The room temperature is compared with a target. When the room is below target, the heater turns on and warms the room. When the target is reached, the heater turns off. The room temperature hovers around or converges on the target ("seeks" the goal).

[b3] A stock-and-flow model of a tank. The water level is the stock. The inlet adds water and the drain removes it. If inflow exceeds outflow, the level rises. Otherwise (outflow at least inflow) the level falls.

[b4] An inventory control loop with a delay. When inventory is below target, an order is placed. Deliveries arrive 2 weeks after ordering. Because of the lag, the orderer keeps ordering while earlier orders have not yet arrived, so the total ordered overshoots (over-ordering). Inventory therefore oscillates around the target instead of settling (overshoot, then excess, then under-ordering, and so on).

[b5] A linear pipeline of sequential steps: collect data, then clean it, then analyze it, then publish the results. There are no loops or branches.

[b6] A request-handling flow with a conditional. Each incoming request is checked. If it is valid, it is processed. Otherwise it is rejected and the sender is told (guess: told of the rejection).

[b7] A fork-and-join workflow. An order is split into two parallel tasks, packing and billing. When both are finished, the order is shipped. Shipping waits for both (join).

[b8] A population model with two loops. Reinforcing loop: births raise the population, and a bigger population produces more births, so it grows. Balancing loop: a larger population cuts the available rations (food, resources per head), fewer rations raise deaths ("cut deaths cut population" probably means that reduced rations lead to more deaths, guess), and that reduces population. The population grows and then levels off at a carrying capacity ("seeks capacity"), probably in an S-shaped curve.

[b9] A retry process with escalation. Try the job. If it fails, wait and then retry. After 3 failures, stop retrying and send it to human review. If the job succeeds, it presumably ends (guess).

[b10] A factory flow with three stages: intake, assembly, inspection. Parts come from suppliers into intake, then to assembly, then to inspection. Items passing inspection are finished and go to customers. Defective items go back from inspection to assembly for rework (a rework loop).

DIFFICULTY: 3, The most confusing part was the b8 phrase "population cut rations cut deaths cut population", where "cut" seems to mean something other than "reduce" in the chain (rations cut deaths contradicts the intended logic).
