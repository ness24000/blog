# A simple Flask-based blog

**Table of contents**
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Documentation](#documentation)
  - [Tests](#tests)
  - [License](#license)

## Overview

This is a simple **Flask-based blog application**. It includes *extended* **markdown** support (e.g. tables, math) and complete **newsletter** logic via email. It serves as the [author's blog](https://txtos.eu), and as playground to learn stuff🛝. 

A key guiding principle is to keep the code as simple as possible. This mostly means avoiding bloating it with software that can do a thousand things in order to get one small thing done. 

## Requirements

You should have `git`, `docker` and `docker-compose`. 

## Setup

To get the blog up and running:

1. **Clone** the repository.
2. **Define environment variables.** Run `cp sample.env .env`, and adapt `.env`. You must define at least: 
   - `ADMIN_KEY` and `DOMAIN_NAME`. Set domain name to `localhost:8080` for local development. 
   - If you use [mailgun](https://www.mailgun.com/) as your email provider: `MAIL_USERNAME`, `MAIL_API_KEY`. Otherwise, you may need to adapta these variables to your email provider. 
3. **Start the application.** Run `docker compose up`. 

Optionally you may also:

4. (Production only) **Set up web server.** A web server to work as reverse proxy is not included (e.g. nginx, traefik). The blog is designed to work with such added layer, though. You will have to handle this yourself based on your deployment tool of choice.  
5. **Personalize.** Since this project is intended as the [author's blog](https://txtos.eu), some bits of the code (e.g. `app/static/`) contain graphics and words irrelevant to the general user. This should likely be changed. 

## Documentation 

Since the admin is assumed to be computer savvy, and in trying to keep the blog as lightweight as possible, all *admin tasks* are accessed via a `url`. 

- **Adding a post:** `DOMAIN_NAME/add_post`
- **Editing a post:** `DOMAIN_NAME/edit_post`
- **Deleting a post:** `DOMAIN_NAME/edit_post`

Once any of these routes are accessed, the frontend is clear enough.

## Tests

Tests are crucial, but writing tests is a terrible way to spend your free time🛝. Since this is a hobby project, it so far has no tests. 

## License

**This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).** You are free to share and adapt the code for non-commercial purposes; commercial use is not permitted.

See the included `LICENSE` file for details and a link to the full legal text.


