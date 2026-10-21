## Decode
[b1] More customers bring more referrals, and more referrals bring more customers. This is a closed reinforcing loop (each change feeds itself and escalates); "forever" says it keeps escalating without end.
[b2] The room temperature is compared with a target. When the room is below the target, the heater is turned on and it warms the room. When the target is reached, the heater is turned off. This is a balancing loop that pulls the room toward the target and settles there.
[b3] The tank level is a stock (it accumulates). The inlet is an inflow and the drain is an outflow. The level rises while inlet flow exceeds drain flow and falls while the drain exceeds the inlet.
[b4] When inventory is below its target, an order is placed. The order arrives late, after a delay of 2 weeks, so (because of the delay) the system over-orders. The result is that inventory swings (oscillates) around the target.
[b5] Collect the data, then clean it, then analyze it, then publish the results, each step starting only after the previous one finishes.
[b6] Check the requests, then: if a request is valid, process it; otherwise reject it and then tell the sender (reject first, then tell, in order).
[b7] An order is split into two parallel activities, packing and billing. When both are done (joined, waiting for all), the order is shipped.
[b8] Two loops. (1) More births bring a larger population, and a larger population brings more births: a reinforcing loop (grows). (2) A larger population brings fewer rations (per capita), fewer rations bring more deaths? No: by the spec, "cut" means more rations bring fewer deaths, so fewer rations bring more deaths, and more deaths bring a smaller population. Thus more population leads to fewer rations, more deaths, less population: a balancing loop that seeks capacity (settles at the carrying capacity).
[b9] Try the job. If it fails: wait, then retry (flow back to the attempt). After 3 failures, escalate to human review.
[b10] Parts go from suppliers to the factory, a system with subsystems intake, then assembly, then inspection (entering at intake and leaving from inspection), and then to customers. Defects flow back from inspection (the factory's flow) to assembly for rework.
## Encode
[h1] stress cut sleep cut stress, grows
[h2] bank account balance stock, deposits in, withdrawals out, fees out; each month: balance lift interest, interest in
[h3] message to queue; queue full: drop message, else worker picks up, processes, result to storage
[h4] demand vs supply; above: price rises; price cut demand cut price, seeks equilibrium; price lift supply lag cut price, seeks equilibrium
DIFFICULTY: 4 and one sentence: the hardest part is the sparse placement rules for lag, vs, and mixed lift/cut loops (and the cut sign in chains like b8), since the spec gives little guidance on where to put them or how to encode proportional or conditional flows.
