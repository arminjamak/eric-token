[b1] Customers produce referrals, and referrals bring in more customers. Each new customer produces more referrals, so the loop feeds itself and grows without limit (reinforcing loop, unbounded growth). Nothing in the description caps it.

[b2] A room is compared against a target temperature. When the room is below target, the heater turns on and warms the room. When the target is reached, the heater turns off. This is a balancing loop that keeps the room near the target. (guess) The room presumably drifts back down when the heater is off, which is what triggers the heater again.

[b3] Tank level is a stock, an amount that accumulates over time. Inflow adds to it and outflow (drain) removes from it. The level rises when inflow exceeds outflow and falls when outflow exceeds inflow. The text does not say whether the level affects either flow.

[b4] Inventory is compared against a target. When it is below target, an order is placed. The order takes 2 weeks to arrive, so during that wait the stock still looks low and more orders get placed, which is over-ordering. When the delayed stock finally arrives, the level overshoots, and the cycle repeats. The result is oscillating swings caused by the delay in the feedback. (guess) The order size is presumably whatever restores the target.

[b5] A one-way pipeline with no loops. Data is collected, then cleaned, then analyzed, then the results are published. Each step starts when the previous one finishes.

[b6] Incoming requests are checked for validity. If valid, the request is processed. If not valid, it is rejected and the sender is told. Each request ends in one of these two outcomes. (guess) The sender is notified only on rejection, since the text mentions telling the sender only in that branch.

[b7] Packing and billing run in parallel, at the same time. Shipping waits until both are complete, so it is a join or synchronization point. Only after packing and billing are both done does the order ship.

[b8] Two loops. The first is a reinforcing loop: births raise population, and a larger population produces more births, so it grows without limit (runaway) unless something else acts. The second is a balancing loop: a larger population lowers rations per person, and lower rations raise deaths (the text's "lowers rations lowers deaths" is read as: each "lowers" means an increase in the first item makes the next one smaller, so fewer rations means more deaths). More deaths lower the population. Because the chain has three negative links, it is a balancing loop that pushes population back down. (guess) "Balancing at capacity" means the population settles near the level that the available food supports.

[b9] A job is tried. If it fails, the system waits and then retries. After 3 failures, the job goes to human review, which is an escalation. (guess) A success presumably ends the process, and the wait duration is not stated.

[b10] Parts flow in one direction: suppliers, then the factory (intake, then assembly, then inspection), then customers. Defects found go back to assembly for rework, which is a feedback loop. (guess) The defects come from inspection, since that is the stage that finds them.

DIFFICULTY: 4
What confused me most was b8, specifically reading "population lowers rations lowers deaths lowers population" as a chain where each "lowers" is a sign, so I had to work out that the loop balances.
