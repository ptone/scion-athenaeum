#Project premise

To demonstrate a system where multiple agents work together to solve a large problem I want to use the scenario of a Fantasy Adventure game Where multiple players (6-10 players) each with different skills and capabilities Work together as a group, Dungeons & Dragons, style To achieve a quest.

In particular several of these character types can "spawn" helper entities to do work (these are represented in the agent system as ephemeral worker agents on some task)

main game characters can also summon expert agents (spawn agents of type oracle, or healer)

In this scenario each character runsAs a deep agent powered by a harness such as Gemini CLI or Claude code

Each agent has a set of skills And the system prompt to Define it as a character

The scenario the quest involves some challenge that requires them To manipulate some files write some code Do some sort of web research Etc

It should involve something where they can split up to each solve Part of the problem on their own And then come back together

And overall should involve a sequence Chapters acrossDifferent land

There is an overall "game runner" agent (similar to a dungeon master), that helps set the scene, sets the quest in motion etc

Some of this game context would be in a shared workspace agents.md file, or in a "game-context.md" file




