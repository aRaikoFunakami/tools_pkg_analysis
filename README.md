# Project Name

This repository is a personal tool designed to assist with specific tasks.

## Introduction

This repository contains a set of personal tools developed for various tasks, including data filtering and total calculation.

## Usage

### Setting up

```bash
poetry install
```

### Configuration  

Before running the scripts, please update the necessary settings in `config.py` to match your environment.

### Commands

To run the tools, use the following commands:

```bash
# To filter data
poetry run python filter.py

# To calculate totals from the specified CSV file
poetry run python calculate_totals.py <outputfile by filter.py>.csv
```