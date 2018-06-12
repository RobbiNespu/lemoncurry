lemoncurry (always all-lowercase) is a Django-based personal site designed to
operate as part of the [IndieWeb][]. It currently supports the following
IndieWeb specifications natively.

- All content is exposed using standard [microformats2][] markup, making it
  easy for other sites and applications across the IndieWeb to consume.
- Additionally, the site owner's profiles are exposed using [rel-me][],
	enabling independent verification of their identity across various services.
	This permits [IndieAuth.com][] to authenticate the site's owner using a
	social profile, such as a Twitter account. However, this functionality is not
	necessary because lemoncurry also fully implements…
- [IndieAuth][], an protocol derived from OAuth 2.0 which enables the site's
	owner to authorise access to their domain directly from the lemoncurry site
	itself. Additionally, tokens for further access to the lemoncurry site may be
	requested and issued, including customisable token scope as in OAuth.
- [Micropub][] is *partially* supported - using a token obtained through
	IndieAuth, clients may post new content to the lemoncurry site using either
	the form-encoded or JSON request formats. There is currently no support for
	updating or deleting existing content through Micropub, although this is of
	course planned.
- [Webmention][], used to enable rich commenting and social interaction between
	separate IndieWeb sites, is partially supported. lemoncurry will correctly
	*send* webmentions to all URLs mentioned in a published entry. However, it
	currently does not expose an endpoint for *receiving* webmentions.
- [WebSub][] is also partially supported. When content is posted through
	Micropub, WebSub is pinged as it should be - however, since only creating
	*new* content through Micropub is supported, updates do not currently cause a
	WebSub ping.

[IndieAuth]: https://www.w3.org/TR/indieauth/
[IndieAuth.com]: https://indieauth.com/
[IndieWeb]: https://indieweb.org/
[microformats2]: http://microformats.org/wiki/microformats2
[Micropub]: https://www.w3.org/TR/micropub/
[rel-me]: http://microformats.org/wiki/rel-me
[Webmention]: https://www.w3.org/TR/webmention/
[WebSub]: https://www.w3.org/TR/websub/

# Requirements

lemoncurry uses the following tools:

* [Pipenv][] - developed with Pipenv 2018.5.18, but should work with most versions.
* [Yarn][] - again, developed with Yarn 1.7.0, but should work with most versions.

As well as the following services:

* [PostgreSQL][] - create a database named `lemoncurry`. Socket auth is
  recommended, so ensure the UNIX user you'll be running lemoncurry with has
	access to that database. Alternatively, set the `POSTGRES_PASSWORD`
	environment variable to use password auth.
* [Redis][] - lemoncurry expects to find Redis on port 6380, rather than the
  standard port of 6379. Sorry about that.

If you're running in production, I'd recommend [Gunicorn][], which is already part
of lemoncurry's Pipfile. Ensure you run Gunicorn behind a secure reverse proxy,
such as [Nginx][].

If you're running in development, the usual Django `run_server` command should
be fine.

[Gunicorn]: https://gunicorn.org/
[Nginx]: https://nginx.org/en/
[Pipenv]: https://docs.pipenv.org/
[PostgreSQL]: https://www.postgresql.org/
[Redis]: https://redis.io/
[Yarn]: https://yarnpkg.org/

# Installation

Clone the repo, and then install both Python and Node dependencies:

```shellsession
$ git clone https://git.00dani.me/00dani/lemoncurry
$ cd lemoncurry
$ pipenv install
$ yarn install
```

Once those steps complete, you should be able to perform the usual Django steps
to get a development server up and running. (If you'd prefer, you can use
`pipenv shell` to activate lemoncurry's virtualenv, rather than prefacing each
command with `pipenv run`. I like being explicit.)

```shellsession
$ pipenv run ./manage.py migrate
$ pipenv run ./manage.py collectstatic
$ pipenv run ./manage.py runserver 3000
```
