# Contributing

Thanks for helping improve this project.

## Before You Start

- Read the [README](README.md) to understand the current architecture and run instructions.
- Check the existing [issues](https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/issues) and [discussions](https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/discussions) to avoid duplicating work.
- If your repository hosting does not expose those relative paths, replace them with your GitHub issue and discussion URLs.

## How to Contribute

1. Open or comment on an [issue](./issues) for bugs, feature requests, or documentation fixes.
2. Start a [discussion](./discussions) for larger design changes, new agents, or workflow changes.
3. Fork the repository and create a focused branch.
4. Keep changes small and aligned with the existing LangGraph, FastAPI, and Streamlit structure.
5. Update tests, docs, and examples when behavior changes.

## Roadmap

This roadmap is ordered by impact and implementation effort. Each item includes the primary files to change first.

### High Priority

| Enhancement | Why it matters | Primary files |
| --- | --- | --- |
| Query controls in the UI | Lets users narrow the analysis and reduces irrelevant output. | [ui/streamlit_app.py](ui/streamlit_app.py), [api/main.py](api/main.py), [graph/workflow.py](graph/workflow.py) |
| Response history or persistence | Turns the app from a one-shot demo into a usable research tool. | [api/main.py](api/main.py), [ui/streamlit_app.py](ui/streamlit_app.py), new [storage/](storage) or [data/](data) module |

### Medium Priority

| Enhancement | Why it matters | Primary files |
| --- | --- | --- |
| Streaming or staged rendering | Shows progress per agent and improves perceived speed. | [ui/streamlit_app.py](ui/streamlit_app.py), [api/main.py](api/main.py) |
| Validation or critic step | Catches weak summaries before the user sees them. | [graph/reducer.py](graph/reducer.py), [graph/workflow.py](graph/workflow.py), new [graph/critic.py](graph/critic.py) |
| Tavily response caching | Cuts repeat calls and lowers latency and cost. | [tools/tavily_search.py](tools/tavily_search.py), new [tools/cache.py](tools/cache.py) |
| Automated tests | Protects the workflow as prompts and agents evolve. | new [tests/test_api.py](tests/test_api.py), [tests/test_workflow.py](tests/test_workflow.py), [tests/test_tools.py](tests/test_tools.py) |
| Deployment separation | Makes backend and frontend easier to host independently. | [api/main.py](api/main.py), [ui/streamlit_app.py](ui/streamlit_app.py), [run.ps1](run.ps1) |

### Low Priority

| Enhancement | Why it matters | Primary files |
| --- | --- | --- |
| Stronger UI polish | Improves presentation but does not change core capability. | [ui/streamlit_app.py](ui/streamlit_app.py) |
| Long-term memory with a vector store | Useful for follow-up research, but not required for the current news workflow. | new [memory/](memory) or [storage/](storage) package, [graph/state.py](graph/state.py), [graph/workflow.py](graph/workflow.py) |
| Additional search providers | Broadens coverage if Tavily is not enough. | [tools/tavily_search.py](tools/tavily_search.py), new [tools/search_providers.py](tools/search_providers.py) |
| Export formats such as Markdown or PDF | Helpful for sharing reports, but not essential for the first stable release. | [api/main.py](api/main.py), [ui/streamlit_app.py](ui/streamlit_app.py) |

## Extending the Project

The codebase is designed to grow in small, composable steps. A practical extension path is:

1. Harden the backend in [api/main.py](api/main.py) with structured responses and clearer failure handling.
2. Improve evidence quality by threading citations from [tools/tavily_search.py](tools/tavily_search.py) through the agents and reducer.
3. Add UI controls and staged progress updates in [ui/streamlit_app.py](ui/streamlit_app.py).
4. Introduce testing and caching support before adding more agents or memory layers.
5. Only then expand the workflow in [graph/workflow.py](graph/workflow.py) with new specialist nodes or critic stages.

## Enhancement Ideas

If you want to improve the system further, the roadmap above is the recommended implementation order. Start with the high-priority items before moving into medium and low priority work.

## Pull Request Guidelines

- Describe the change clearly and link the related issue or discussion.
- Include screenshots or sample output if the UI or report format changes.
- Keep the pull request scoped to one purpose when possible.
- Verify the app still runs with the updated requirements and launch script.

## Issue and Discussion Links

- [Open an issue](https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/issues/new)
- [Start a discussion](https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/discussions/new)

If your hosting platform requires full URLs, you can use the direct links for this repository:

- https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/issues/new
- https://github.com/ARUNAGIRINATHAN-K/parallel-news-analyst/discussions/new
