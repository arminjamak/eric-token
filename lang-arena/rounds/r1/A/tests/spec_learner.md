## Decode
[b1] More customers cause more referrals, and more referrals bring more customers: a self-amplifying (reinforcing) loop, with no limit on the growth.
[b2] The room temperature is compared to the target. If it is colder than the target, the heater turns on and raises the temperature; if it is at the target, the heater turns off. This is a balancing loop that pulls the temperature back toward the target.
[b3] The water level in the tank is a stock. Water flows in through the inlet (inflow) and out through the drain (outflow). If inflow exceeds outflow, the level rises; if inflow is below outflow, the level falls.
[b4] If inventory is below the target, the shop places orders. Delivery arrives after a 2-week delay, so the shop over-orders, and inventory oscillates around the target (a balancing loop with delay).
[b5] Steps in strict sequence, each starting only after the previous finishes: collect data, then clean it, then analyze it, then publish the results.
[b6] Each incoming request is checked. If it is valid, it goes to processing; otherwise it is rejected and the sender is notified (reject first, then notify).
[b7] An order splits into two parallel paths run at the same time: packing and billing. When both are done, then shipping starts.
[b8] More population causes more births, which cause more population: a reinforcing loop. More population causes less food each, which causes a higher death rate, which causes slower growth: a balancing loop. Population levels off at the carrying capacity (the limit).
[b9] Attempt the job. If it fails, wait, then retry. After 3 failures, it goes to human review.
[b10] A factory is a system with three subsystems: intake, assembly and quality check. Parts flow from suppliers to intake to assembly to quality check. Finished products go to customers. Defective ones return back to assembly (rework).
## Encode
[h1] more stress, less sleep, more stress: reinforcing loop. keeps getting worse.
[h2] bank account balance is stock: deposits to balance; balance to withdrawals, fees. each month, interest to balance, more balance, more interest: reinforcing loop.
[h3] message to queue. if queue full, message dropped; else worker picks up, processes, writes result to storage.
[h4] if demand over supply, higher prices. higher prices, less demand. higher prices, after delay, more supply, lower prices: balancing loop. prices pulled back toward equilibrium.
DIFFICULTY: 4 - The hardest part is that the spec leaves open how to express things it has no word for (e.g. "vicious cycle keeps getting worse," a loop's polarity or target, interest proportional to balance, and when a comparative chain is a loop versus a one-way cause).
