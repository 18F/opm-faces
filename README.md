# opm-faces

## Report
Our final report and recommendations may be found on [18F's Google Drive](https://drive.google.com/open?id=0B8u6AetkKiTUM0RIVEZZbkI2WTQ).

## Magic Rules!
As part of our engagement, we created a very basic prototype business rules calculator to demonstrate
a few of the concepts and patterns that were included in our recommendations:
 - Store rules as data, not as code
 - Choose a single, consolidated place for calculations to be executed
 - Loosen up coupling between the calculation engine and any front end components to allow for component switch out

To run Magic Rules, just clone this repository to your local machine navigate to `/magic_rules` and execute
`magic.py`. The various data types ("prototypes", "calculations", and "rules") are written to `/magic_rules/datastore`
when created via the web interface. Magic Rules also has a simple read/write API that is documented in `/api/`.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
