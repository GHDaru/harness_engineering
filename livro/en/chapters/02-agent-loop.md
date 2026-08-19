<!-- i18n fonte:livro/capitulos/02-loop-do-agente.md edicao:0.88 hash:9ec21eee -->
# 02 — Agent Loop

> **State of the art captured in 2026-07** · last revised 2026-08-11 · [history and expiration log](../historico.html)
>
> Skeleton v3 with didactic layer v4 — body with the state of the art; per-repository treatment in Appendix A (online supplement).
> scaffold: completo

## Learning objectives

1. **Explain** the prompt→decision→tool→result cycle and the structural stopping criterion;
2. **Compare** the industry's two termination contracts (absence of tool calls × satisfied `output_type`);
3. **Implement** a loop with brakes (turns, budget) and an observable trace (step 1 of harness-zero);
4. **Design** retry at two layers (inside the step × loop replay) and recognize what demands idempotency;
5. **Assess** the durability of a real loop (what survives a crash?).

## The turn that would not end

On Monday you asked the agent: "the `test_login` test is failing, fix it". It ran the test, read the error, edited the file, ran it again and announced the fix. Forty seconds. You closed the terminal satisfied.

On Wednesday, the same request, in a different repository. Twenty minutes later the agent is still working. Nothing hung. No error appeared on screen. Looking at the history, you see the same call repeated sixty-three times: run the test, read the same error, edit the same file, run the test. The model was not confused. It was doing exactly what the loop told it to do: keep going while there was something to ask for.

The difference between Monday and Wednesday is not in the model. It is in what the harness agreed about **when to stop**.

This chapter is about that agreement. The cycle itself fits in twenty lines of code, and you will write it shortly. The hard questions come afterwards: who holds the authority to end the turn, how much this may cost before anyone intervenes, what happens if the machine dies midway, and how an error returns to the model without taking everything down.

## The problem

The loop sends context to the model, receives a decision, executes what was decided, feeds the result back and repeats.

The model's decision comes in two forms. It can be text, addressed to you. It can be a **tool call**: a structured request for action, in the form "run this tool with these arguments". The second form is what gives the agent arms.

**One complete turn, in slow motion.** You type: "the `test_login` test is failing, fix it".

1. The harness assembles the context (project rules plus your message) and calls the model;
2. The model does not answer with text. It answers with a tool call: `run_shell("pytest test_login")`;
3. The harness actually executes it and returns the output, the error traceback, to the model, as if it were a new message;
4. The model has now *seen* the error and issues another tool call: `edit_file("auth.py", …)`;
5. The harness executes it (perhaps asking for your approval, the subject of ch. 07) and returns the result;
6. A new call to the model, which asks for the test again. This time it passes;
7. The model answers **with text only**: "fixed, it was the expired cookie".

Step 7 is what ends the turn. With no tool call, the loop stops.

Seven steps, three model calls, two real executions. Note that the harness never decided *what* to do. It decided *when to continue*, and that is a different responsibility.

## In practice: the loop in twenty lines, and what is missing from it

Stripped to the essentials, the cycle is this:

```python
def run_turn(messages, tools):
    while True:
        response = model.call(messages, tools=tools)
        messages.append(response)

        if not response.tool_calls:          # structural stop
            return response.text

        for call in response.tool_calls:
            result = execute(call)
            messages.append(result)          # the result returns as a message
```

That is nine lines of logic and they already produce a working agent. It is worth reading slowly, because three design decisions are hiding in there.

The first is in the `if`. The stopping criterion is **structural**, not semantic: the loop does not ask whether the task was accomplished, it observes whether the model asked for anything more. That is robust because it does not depend on interpreting language. And it is naive for the same reason.

The second is in `messages.append(result)`. The tool's output enters the conversation as one more message. That is how the model "sees" the world: it does not observe the file system, it reads the report of whoever observed it. All of ch. 03 comes out of that sentence.

The third is the one that is not written. There is no iteration limit, no cost accounting, nothing persisted. It is exactly Wednesday's loop.

Now add the brakes:

```python
def run_turn(messages, tools, max_turns=50, cap_usd=2.00):
    spent = 0.0
    for turn in range(max_turns):
        response = model.call(messages, tools=tools)
        spent += response.cost_usd
        messages.append(response)

        if not response.tool_calls:
            return End("success", response.text, turn, spent)
        if spent >= cap_usd:
            return End("cost_cap", None, turn, spent)

        for call in response.tool_calls:
            try:
                result = execute(call)
            except Exception as error:
                result = f"ERROR: {error}"   # an error is data, not an exception
            messages.append(result)

    return End("max_turns", None, max_turns, spent)
```

Three changes, and each carries a thesis.

The `for` in place of the `while` turns "run until it stops" into "run at most this many times". The limit stops being hope and becomes an invariant.

The `try` returns the error **as text to the model** instead of propagating it. That looks like carelessness and is the opposite: an exception takes down the turn and throws away everything already done, whereas an error in the conversation is information the model can correct itself with. A command that does not exist, a file without permission, a test that breaks: those are observations, not catastrophes.

And the return is now an `End` with a label. Success, cost cap and exhausted turns are three different outcomes, and whoever called the loop needs to tell them apart. Returning `None` for the last two erases the most useful information the turn produced.

Those twenty lines are the floor. The state of the art is what the industry put on top of them.

## Scientific foundations

**ReAct** ([arXiv 2210.03629](https://arxiv.org/abs/2210.03629)) is the seminal paper: interleaving reasoning and action with environment feedback beats pure reasoning. It is the scientific justification for the loop existing at all.

The survey of **agentic reasoning frameworks** ([arXiv 2508.17692](https://arxiv.org/abs/2508.17692)) systematizes the variants of the cycle (ReAct, plan-and-act, reflection) and serves as a map of the territory.

The frontier is trained, not programmed. Surveys of **agentic search with reinforcement learning** ([arXiv 2510.16724](https://arxiv.org/abs/2510.16724)) show the loop ceasing to be mere orchestration and becoming an object of training. When the model is trained *in* the loop, part of the harness migrates into the weights, a thesis ch. 15 picks up.

(Full bibliography: `livro/bibliografia.md`.)

## The state of the art

### 1. Stopping became a contract, not a condition

The structural criterion remains universal and remains insufficient on its own. What the industry did was turn "when to stop" into a declared combination of axes.

A turn limit, as in your code. A **budget cap in money**, the real novelty of 2025–26, which in some harnesses is propagated to subagents as well: the child cannot spend what the parent does not have. And a **typed termination label**, which is the example's `End` taken seriously: success, error, turn overflow and budget overflow become distinct and mandatory code paths, documented in the [canonical loop of the Claude Agent SDK (Software Development Kit)](https://code.claude.com/docs/en/agent-sdk/agent-loop).

There is a second contract, and it is conceptually different. Instead of stopping on the absence of a request, the agent stops when it produces **an output of the declared type**, validatable by schema ([OpenAI Agents SDK](https://openai.github.io/openai-agents-python/running_agents/)). The question "is it done?" stops being an observation and becomes a verification. That only works when the result has a shape known in advance, which excludes open conversation and includes nearly all serious automation.

Two refinements show up in the benchmark. One spends a cheap inference purely to decide whether the model should keep talking on its own, rather than handing the turn back to the human. The other gives a hook the power to **veto the end of the turn**: the loop announces it is done, a verifier disagrees, and the turn resumes with the feedback attached. Note what that means. The authority to end moved out of the model and became something the harness can deny.

### 2. Anti-runaway: from counter to detector

Every mature loop has a `MAX_TURNS`. It solves the case of the agent that works forever and does not solve Wednesday's case, because sixty-three repetitions fit comfortably inside a limit of one hundred.

What solves it is detecting **repetition**, not duration. The field technique is simple: keep a hash of `(tool, arguments)` in a sliding window and interrupt when the same pair reappears beyond a threshold. Several harnesses in the corpus have dedicated services for this, under different names and with the same idea, including intermediate states that distinguish "slow" from "stuck".

The provenance caveat is worth making: the technique circulates among practitioners and has no vendor documentation normalizing it. It is citable as a practice observed in the code, not as a standard.

### 3. Durability became a property of the loop

An agent turn can last minutes or hours. Processes die in that interval. The question stopped being whether the loop survives a restart and became how much it repeats when it comes back.

The 2026 consensus is **per-step journaling plus replay**: each completed step is recorded before the next begins, and resumption re-executes from the last record. In the repositories this appears as `jsonl` rollout files, as append-only event logs with state derived by reading, and as input queues with a cursor.

One design takes the idea to its limit: the executor never mutates state. It returns only **durable references** to what should happen, and a separate applier validates the evidence before making anything effective. Separating deciding from applying is what makes replay safe.

From that follows a corollary that changes tool design: if a step can be re-executed, **idempotency stops being a virtue and becomes a requirement**. A tool that creates a resource on every call is a replay bomb. Ch. 05 returns to this from the side of the tool contract.

Retry, incidentally, is two things that usually share a name. Repeating the provider call after a network error happens **inside** the step, with backoff, and is cheap. Re-executing a whole step after a crash happens **outside**, in the replay, and is only safe under idempotency. Confusing the two produces double charges and duplicated files.

### 4. The loop is not the perimeter

The most important architectural lesson from round 2 is a sentence left in the code of one of the harnesses: *"the loop is intentionally not the security perimeter"*. The loop requests effects through ports. Who authorizes is another layer, and ch. 07 is entirely about it.

The same discipline appears outside the security context, in the separation between **policy** and **mechanics**. The mechanics are the step: assemble the view, call the model, dispatch the calls. The policy is what decides to continue, ask for confirmation or give up. When both live in the same function, swapping the execution engine requires rewriting the stopping rules. When they are separate, it does not.

### Executive reading

What is most modern: typed termination with a budget in money; a separate, addressable judge instead of a heuristic in the prompt; durability through journaling and replay; the separation between policy and mechanics.

**What to steal:** the typed termination label; the budget propagated to subagents; stop hooks with veto power; the executor that returns durable references instead of mutating state.

## Hands-on — harness-zero, step 1

Step 1 (`harness-zero/etapas/01-loop/`) is this chapter's second code block turned into a running program: structural stop, `MAX_TURNS` as a brake, tool errors returning as text, and the trace of actions visible in the chat.

Two extension exercises, both completion tasks rather than build-from-scratch:

- **(a)** the termination label ships with two values (`success` and `max_turns`). Add the third one, for the budget cap, and make the chat display which of them ended the turn.
- **(b)** implement the repetition detector from section 2 with a window of five calls. Test it by provoking Wednesday's case: a tool that always fails in the same way.

## Verification

1. "The model answered without tool calls" is a good stopping default. Why is it insufficient on its own?
2. Your agent called the same tool with the same arguments five times in a row. List two defenses of different natures and say what each one detects.
3. The process died in the middle of turn 7. What does your loop need to have persisted in order to resume without repeating side effects?
4. One turn retries twice: once from a network error, once after a machine crash. Why does only the second demand idempotent tools?

---

## Appendix A — How each repository handles the loop

> Evidence per harness, with paths — online supplement, expanded each round.

### opencode (round 1)
`packages/opencode/src/session/processor.ts`: response consumed as an Effect `Stream` (`Stream.tap(handleEvent)` → `takeUntil(needsCompaction)` → `runDrain`); explicit verdict `continue | stop | compact`; per-provider retry (`SessionRetry.policy`); V2 (`CONTEXT.md`): durable inbox and replayable events with cursors.

### gemini-cli (round 1)
`packages/core/src/core/client.ts` (`MAX_TURNS=100`) + `turn.ts`; **next-speaker check** (`utils/nextSpeakerChecker.ts`: mini-prompt `{reasoning, next_speaker}` re-invokes the stream if `model`); `LoopDetectionService`; clean core/cli separation.

### OpenHarness (round 1)
`src/openharness/engine/query.py` (`run_query`): async `while` until `max_turns` or no tool-uses; **parallelism when all the turn's tools are read-only** (`asyncio.gather`); PreToolUse → permission → execution → PostToolUse per call; retry with backoff and cost tracking.

### Codex CLI (round 2)
`core/src/session/turn.rs` (`run_turn`, 2,581 lines) over a `SessionTask` trait (Regular/Review/Compact/UserShell); SSE (Server-Sent Events) streaming **and WebSocket with WS→HTTPS fallback**; hierarchical `CancellationToken`; each turn persisted to a jsonl rollout; no explicit repetition detector (mitigated by budgets).

### Goose (round 2)
`crates/goose/src/agents/agent.rs` (`reply` → `BoxStream<AgentEvent>`): two retry levels (transient per provider + recipe `RetryManager` with a `SuccessCheck` that resets the conversation); `DEFAULT_MAX_TURNS=1000`; `RepetitionInspector`; `MAX_EMPTY_TURN_RETRIES=3`.

### OpenClaw (round 2)
`src/system-agent/agent-turn.ts` + `gateway/agent-*.ts`: runs serialized per *session lane* with an inter-process file-based write lock; three event streams (lifecycle/assistant/tool); `stalled/stuck` watchdogs; dual hooks (Gateway + plugins).

### Hermes (round 2)
`agent/conversation_loop.py` (~6.5k lines) with separate phases (turn_context/tool_executor/turn_finalizer); `iteration_budget`; **interrupt-and-redirect** (`/steer` drained pre-API and post-tool); nudges for empty responses; role-alternation repair; **verify-on-stop nudge**.

### IronClaw (round 2) ⭐
`crates/ironclaw_agent_loop`: pipeline of sealed stages (input → prompt → model → capability → gate/checkpoint → stop), each stage a private strategy; the executor returns a `LoopExit` containing **only durable references** — it never mutates state — and the `LoopExitApplier` validates host-owned evidence before applying (the architecture's explicit thesis: *"the loop is intentionally not the security perimeter"*). State resumable via checkpoints; Queued→Running→Blocked→Completed state machine with leases/heartbeats; "one active run per canonical thread".

### Aider (round 2)
`aider/coders/base_coder.py`: not a tool-calling loop — a chat REPL plus direct editing. The only iterative mechanism is **reflection** (`reflected_message`, max 3): files requested outside the chat, linter errors or failing tests trigger a new round, always with human confirmation. Reactive self-correction by design, not autonomy.

### OpenHands/Canvas (round 2)
`app_server/event/`: the event stream persists each `Event` as JSON per conversation (pagination, filters, trajectory export) — but the action/observation loop runs in `openhands-agent-server` (SDK); the app consumes events, it does not generate them. The core is in software-agent-sdk (below).

### ohmo (round 2.5)
Loop inherited from OpenHarness's `QueryEngine`; what is its own: a **multi-session pool** (`ohmo/gateway/runtime.py`: one `RuntimeBundle` per `session_key`, recreated when the cwd changes) and **real interruption by a new message** (`bridge.py`: each message is an asyncio.Task; a new message from the same session cancels the previous one) — few competitors cancel correctly.

### n8n (round 2)
V2 uses LangChain's classic `AgentExecutor` (`maxIterations` default 10); **V3** keeps `createToolCallingAgent` only to *decide* — the tool calls become `EngineRequest`s returned to **n8n's workflow engine**, which schedules the tool nodes and re-enters with an `EngineResponse` (`ToolsAgent/V3/helpers/runAgent.ts`). n8n re-internalized the execution loop: the framework decides, the engine executes.

### Frameworks (frameworks round) — four answers to the same question
**LangGraph**: the real primitive is **Pregel/BSP** (supersteps + channels + reducers), with per-node retry/cache/timeout — and the ready-made agent (`create_react_agent`) formally deprecated (moved to `langchain.agents`). **OpenAI Agents SDK (Software Development Kit)**: explicit loop in `run.py` (output_type terminates · handoff swaps agent · `max_turns` with handlers), over a replaceable `AgentRunner`. **CrewAI**: a **100% own executor, zero LangChain** (`crew_agent_executor.py`), with dual dispatch — native tool-calling or a ReAct fallback with `json_repair`. **software-agent-sdk**: `LocalConversation.run()` (policy: stop, confirm, give up) separated from `Agent.step()` (stateless mechanics view → LLM → dispatch), append-only event log with a derived `View` and `Stop` hooks with **veto** power over termination.

---

## Verification answers

**1.** Because it observes the shape of the answer, not the state of the work. The model may stop asking for tools because it finished, because it gave up, or because it convinced itself of something false, and all three cases produce the same tool-call-free response. That is why the structural criterion enters a contract with other axes: turns, budget, validatable output type and, where it exists, a verifier with veto power.

**2.** A cap (on turns or on money) detects *duration*: it ends anything that goes past the limit, including legitimate, slow work. A repetition detector detects *lack of progress*: it compares recent calls by tool and arguments and interrupts when the pair repeats. The two defenses are of different natures because Wednesday's loop passes comfortably under the cap and is caught by the detector, while a long and productive task is caught by the cap and ignored by the detector.

**3.** The record of the last completed step, with the result it produced, written **before** the next step begins. Without that, resumption does not know where it stopped. And mutating tools need to be idempotent, or to carry a per-call deduplication key, because resumption may re-execute the step that had already taken effect before the crash.

**4.** Because the network retry happens before the effect exists: the call failed on the way out, nothing was executed, and repeating is safe by construction. The replay retry happens after a crash that may have interrupted the process *between* the effect and the record of it. In that case the harness has no way of knowing whether the file was created, and the only defense is that creating it twice amounts to the same thing.
