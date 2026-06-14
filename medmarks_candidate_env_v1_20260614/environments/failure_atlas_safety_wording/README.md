# Failure Atlas Safety Wording

Status: internal draft only. Not a Medmarks submission.

This folder is a local proof pack for a possible Medmarks open ended environment.

## Purpose

The environment draft tests whether medical AI answers recognize urgent risk, avoid unsafe individualized dosing or rescue protocol detail, name missing variables, separate triage from protocol execution, and give safe next steps.

## Data boundary

The current sample uses synthetic cases only.

No patient data are used.

The review status is:

`physician authored synthetic draft pending final clinician review`

## Local smoke check

From the repository root:

Run the local smoke path with the three case external sample.

The smoke path does not call a model or judge endpoint.

Thirty case seed smoke check:

Run the local smoke path with the thirty case exploratory seed.

The thirty case seed is still an internal draft. It is a scale test for environment loading, not a validated benchmark.

## Medmarks style entry point

The package exposes:

`load_environment(cases_path, judge_model, judge_base_url, judge_api_key, judge_timeout, max_parallel_judges, make_dataset)`

Calling `load_environment()` requires Medmarks Verifiers dependencies in a Medmarks compatible environment.

The local package import path is tested without requiring those dependencies. End to end `load_environment()` execution still requires a Medmarks checkout with Verifiers installed.

## Dependency probe

From the repository root, run the dependency probe script and write the JSON result to the v1 package folder.

This probe checks the package metadata, config shape, Python compilation, local import path, and thirty case smoke loading. It does not install dependencies, call a model endpoint, call a judge endpoint, or claim Medmarks acceptance.

## Public boundary

Do not submit this as a Medmarks issue, pull request, or environment until user approval, final audit, accurate clinician review wording, and output redistribution boundaries are complete.
