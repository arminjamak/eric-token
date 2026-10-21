## Decode
[b1] More customers bring more referrals, and those referrals bring more customers. The two links close into a reinforcing loop (grows): each change feeds the next and the growth escalates upward without limit ("forever").
[b2] The room is compared with the target. When the room is below target, the heater turns on and warms the room. When the target is reached, the heater turns off. The sentence ends in seeks, so this is a balancing loop that pulls the room toward the target and settles there. Seeks has no name after it, so the goal is taken from the comparison with target.
[b3] "Tank level" is a stock: it accumulates, rising while the inlet (an inflow) exceeds the drain (an outflow) and falling while the drain exceeds the inlet.
[b4] When inventory is below target, an order is placed. Ordering acts late by a 2 week lag, so during those weeks ordering continues and the result is over-ordering. The stated outcome is swings, meaning the system oscillates up and down.
[b5] Four steps run strictly in sequence: collect data, then clean, then analyze, then publish results. Each step starts only after the previous one finishes.
[b6] First, check requests. Then, if a request is valid, process it. Otherwise, reject it and tell the sender, in that order. The else case covers both the rejecting and the telling, up to the end of the clause.
[b7] The order splits into packing and billing, which run in parallel. Once both are done (join, waiting for all), ship.
[b8] Two loops appear in this sentence. Loop 1 (grows, reinforcing): births lift population and population lifts births, so more births bring more population, which brings more births, escalating upward. Loop 2 (seeks capacity, balancing): population cut rations, rations cut deaths, and deaths cut population. More population means fewer rations, fewer rations mean more deaths, and more deaths mean less population. The loop settles toward capacity.
[b9] First, try the job. If it fails, wait, then retry. After three failures, send to human review. The sentence gives no wait length. It also does not say whether the third failure triggers review instead of another wait and retry.
[b10] Parts flow from suppliers into the factory. The factory is a system with subsystems in a path: parts enter at intake, then go to assembly, then to inspection, and leave from inspection. From there they flow to customers. Defects flow back to assembly as rework. The sentence does not say where defects come from.

## Encode
[h1] stress cut sleep cut stress, grows; this vicious cycle keeps getting worse
[h2] bank account balance stock; deposits in, withdrawals and fees out; each month: balance lift interest, interest in
[h3] message to queue; queue full: message dropped, else worker picks up message, processes, writes result to storage
[h4] demand exceeds supply: price rise; price cut demand; price lift supply lag cut price, seeks equilibrium

DIFFICULTY: 5, because the hardest part is placing a lag inside a cause chain (the spec defines lag only as a word that makes what came just before act late) and deciding how far an else reaches (to the clause end, which the spec states only in prose).
