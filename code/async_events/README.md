# Asynchronous event handling

## Contents

This is a (successful) attempt at writing event handling code where not all of the event code should be executed in a single cycle, but spread out through multiple game ticks. This can be done with state machine code, but the technique presented here (using generator `yield` to pause function execution) results in simpler linear code. Note that this code can be used inside normal synchronous code without requiring async or await keywords.
