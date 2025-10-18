
#!/usr/bin/env python3
"""CLI entrypoint for eCourts Scraper"""
import json
import click
from scraper import run_check


@click.command()
@click.option('--cnr', default=None, help='CNR number (full)')
@click.option('--case-type', default=None, help='Case type (e.g., CR, RC, etc.)')
@click.option('--case-no', type=int, default=None, help='Case number')
@click.option('--case-year', type=int, default=None, help='Case year')
@click.option('--today', is_flag=True, help='Check listing for today')
@click.option('--tomorrow', is_flag=True, help='Check listing for tomorrow')
@click.option('--causelist', is_flag=True, help='Download full cause list for today')
@click.option('--download-pdf', is_flag=True, help='Download case PDF(s) if available')
@click.option('--out', default=None, help='Output file to save JSON results')
def main(cnr, case_type, case_no, case_year, today, tomorrow, causelist, download_pdf, out):
    """Run checks based on provided options."""
    if not any([cnr, (case_type and case_no and case_year), causelist]):
        click.echo('❌ Provide either --cnr or (--case-type, --case-no, --case-year) or --causelist')
        raise SystemExit(1)

    config = {
        'cnr': cnr,
        'case_type': case_type,
        'case_no': case_no,
        'case_year': case_year,
        'today': today,
        'tomorrow': tomorrow,
        'causelist': causelist,
        'download_pdf': download_pdf,
    }

    results = run_check(config)

    if out:
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        click.echo(f'✅ Wrote results to {out}')
    else:
        click.echo('ℹ️ Saved results to console (use --out to save to file).')


if __name__ == '__main__':
    main()
