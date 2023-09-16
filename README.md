# DAIS RMU

Website of the Discrete Algorithm Insights Seminar at the Rhine-Main-Universities:
[https://dais.rhein-main-universitaeten.de/](https://dais.rhein-main-universitaeten.de/)

## Editing the Website

You can edit the website by using the GitHub web interface or by cloning the repository and editing the files locally.

- The talks are in the directory [`src/content/talks`](src/content/talks). Simply edit an existing file or add a new one.
- The text of the website is in [`src/pages/index.astro`](src/pages/index.astro).

## Local Development

- Install [Node.js](https://nodejs.org/en/download/) (version 20 or higher).
- Install [bun](https://bun.sh/).
- Clone the repository.
- Run `bun install` to install the dependencies.
- Run `bun dev` to start the development server.

## Deployment

Pushing to the `main` branch will automatically deploy the website to [https://dais.rhein-main-universitaeten.de/](https://dais.rhein-main-universitaeten.de/).

## Major Dependencies

The site is built using [Astro](https://astro.build/).
