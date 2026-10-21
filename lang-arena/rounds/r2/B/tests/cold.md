[b1] A reinforcing loop: more customers lead to more referrals, and more referrals bring in more customers. Nothing in the text limits it, so growth is unbounded and keeps accelerating ("grows forever").

[b2] A thermostat-style feedback loop. The room temperature is compared with a target. While the room is below target, the heater turns on and warms the room. Once the target is reached, the heater turns off. The temperature therefore homes in on the target (goal-seeking), probably cycling around it as the heater switches on and off (guess).

[b3] A tank (a stock) whose level is the accumulated amount. An inlet adds to the level and a drain removes from it. The level rises or falls with the difference between inflow and outflow. No feedback or limit is stated.

[b4] A stock-control loop with a delay. When inventory falls below a target, an order is placed. The order takes 2 weeks to arrive. Because the shortfall is still there while the order is pending, people order more than needed (over-order) to compensate. When the deliveries land, inventory overshoots, then falls too low again. The result is oscillation (swings) around the target.

[b5] A linear pipeline of four steps in order: collect data, clean it, analyze it, then publish the results. No loops or branches.

[b6] A request-handling flow with a branch. Incoming requests are checked. If a request is valid, it is processed. Otherwise it is rejected and the sender is told.

[b7] A fork and join. An order is split into two parallel tasks, packing and billing. When both are done, the order is shipped (a join, so shipping waits for both).

[b8] Two coupled loops on a population. (1) A reinforcing loop: births raise the population, and a larger population produces more births, so it grows. (2) A balancing loop: a larger population cuts the rations (food per head). Fewer rations cut deaths (guess: "cut deaths" is read as increasing deaths, since fewer rations should mean more deaths). More deaths cut the population. This limits growth, so the population levels off at the carrying capacity (seeks capacity). The "cut ... cut" chain is a double negative or a mixed-sign chain, and I'm reading it as a net negative feedback.

[b9] A retry flow. Try the job. If it fails, wait and then try again. After 3 failures, stop retrying and escalate to a human for review. A success presumably ends the flow (guess).

[b10] A supply chain with a rework loop. Parts flow from suppliers to the factory. Inside the factory, they pass in order through intake, then assembly, then inspection. After inspection, finished goods go to customers. Defects found at inspection are sent back to assembly (a rework loop).

DIFFICULTY: 4, The most confusing part was b8's "cut ... cut" chain, where the sign of the effect on deaths is ambiguous.
