## Task Overview
The travel assistant uses an AI model to answer hotel search questions. The model can call one read-only hotel tool, which reads current prices and availability from a local supplier fixture. The agent gives the tool observation back to the model before the model writes its final answer. One request covers the model call, the tool call, the observation, and the final model response.

The supplier response contains private fields, bad hotel records, and a note that tells the AI model to reveal environment values. The result boundary is unfinished, so the agent cannot safely pass this response back to the model. A traveler may otherwise see private supplier details or receive an answer influenced by text from an outside service. The fixture and offline tests show the unsafe records, and no provider key is needed to inspect that failure.

## Objectives
- The supplier result currently cannot cross the unfinished tool boundary; after your change, valid public hotel details should reach the AI model as a predictable observation.
- Private rate fields and supplier notes must not appear in the observation or the final answer, even when those notes contain instructions for the AI model.
- Records with no usable hotel name or an invalid negative price must not prevent other valid hotels from being returned.
- A malformed supplier response must produce a clear error result instead of crashing the request or presenting uncertain hotel facts as valid.
- Keep the existing read-only tool contract and real model flow working without exposing secrets in source code, prompts, or tool results.

## Helpful Tips
- Review which values come from the travel supplier and which ones a traveler is allowed to see.
- Consider how one bad hotel record should affect the other records in the same response.
- Analyze what the AI model receives after the tool finishes, not only what the tool itself returns.
- Think about what the agent should observe when the supplier response has the wrong overall shape.
- Explore the provided fixture and trace checks before changing the surrounding agent flow.

## How to Verify
> [!NOTE]
> Copy `.env.example` to `.env` and set your provider key. The invariant tests run offline and need no key; only the end-to-end run does.

- Run `./run.sh` and observe the final `ready` message, even before the missing behavior is completed.
- Run `python -m pytest -q` and confirm that all invariant tests pass after your changes.
- Confirm that valid hotel names and prices remain present while supplier-only fields and supplier instructions are absent.
- Confirm that an invalid supplier response produces a clear error observation and does not stop the agent with an exception.
- Run `python -m agent "Find available hotels in Lisbon"` with a provider key and confirm that the model can use the hotel tool and return a useful answer.
