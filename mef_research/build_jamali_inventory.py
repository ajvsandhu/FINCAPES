"""Rebuild bounded, source-backed inventory. Run from any directory; no network."""
from pathlib import Path
import csv
import hashlib
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'mef_research'
OUT = BASE / 'output/jamali_inventory'
OUT.mkdir(parents=True, exist_ok=True)
RUPTL_URL = 'https://gatrik.esdm.go.id/gatrik/gatrik-api/storage/migrasi/download_index/files/b967d-ruptl-pln-2025-2034-pub-.pdf'
NP_URL = 'https://www.plnnusantarapower.co.id/storage/investor_corporate_statistic/files/G3V6naONEPK3LxhDfZnzuNF2sQxQkqXqXlbTMo93.pdf'

def clean(v):
    return ' '.join((v or '').split())

def num(v):
    v = re.sub(r'[^\d.,-]', '', v)
    return None if not v or v == '-' else float(v.replace('.', '').replace(',', '.'))

def write(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows(rows)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    manifest = json.loads((BASE / 'jamali_inventory_manifest.json').read_text())
    for source in manifest['inputs']:
        path = ROOT / source['path']
        assert sha(path) == source['sha256'], path
    pdf = fitz.open(ROOT / 'grid_data_sources/raw/ruptl_2025_2034.pdf')
    snapshots = {}
    pages = manifest['inputs'][0]['inspected_pdf_pages']
    for n in pages:
        snapshots[f'RUPTL:{n}'] = pdf[n-1].get_text(sort=True)
    np = fitz.open(BASE / 'raw/pln_np_statistics_2024.pdf')
    for n in manifest['inputs'][1]['inspected_pdf_pages']:
        snapshots[f'NP:{n}'] = np[n-1].get_text(sort=True)
    (OUT / 'page_text_snapshots.json').write_text(json.dumps(snapshots, ensure_ascii=False, indent=2)+'\n')

    # A published planning row is a candidate, not a commissioned generator.
    groups = {'DKI': [818], 'Banten': [830,831], 'Jawa Barat': [849,850,851,852],
              'Jawa Tengah': [880,881,882], 'DIY': [901],
              'Jawa Timur': [913,914,915,916], 'Bali': [943,944]}
    planned, raw, reconciliations = [], [], []
    for province, pages in groups.items():
        rows, published = [], None
        for page in pages:
            for table in pdf[page-1].find_tables().tables:
                cells = table.extract()
                header = [clean(v) for v in cells[0]]
                if not ('Sistem' in ' '.join(header) and 'Pengembang' in header):
                    continue
                raw.append({'province': province, 'pdf_page': page, 'cells': cells})
                system = next(i for i,v in enumerate(header) if v.startswith('Sistem'))
                tech = header.index('Jenis')
                name = next(i for i,v in enumerate(header) if v.startswith('Lokasi/Nama'))
                cap = next(i for i,v in enumerate(header) if v.startswith('Kapasitas'))
                ared = next(i for i,v in enumerate(header) if 'ARED' in v)
                status = header.index('Status')
                developer = header.index('Pengembang')
                merged = []
                for physical in cells[1:]:
                    if (not any(clean(v) for v in physical[:system])
                            and any(clean(v) for v in physical[name:cap]) and merged):
                        merged[-1][name] = clean((merged[-1][name] or '') + ' ' + ' '.join(clean(v) for v in physical[name:cap]))
                    else:
                        merged.append(list(physical))
                for r in merged:
                    if any(clean(v) in ('Jumlah','Total') for v in r[:3]):
                        published = num(clean(r[cap]))
                    number = clean(' '.join(clean(v) for v in r[:system]))
                    if not number.isdigit():
                        continue
                    no = int(number)
                    # Some PDF rows split the name into several physical columns.
                    nm = clean(' '.join(dict.fromkeys(clean(v) for v in r[name:cap] if clean(v))))
                    base = clean(' '.join(dict.fromkeys(clean(v) for v in r[cap+1:ared] if clean(v))))
                    # Table detector splits B1.10 across physical rows; checked against
                    # the full page, retained above in raw cells and page-text snapshot.
                    if province == 'DKI':
                        nm = {1:'Sunter',2:'Jawa-Bali (Kuota) Tersebar'}[no]
                        base = str({1:2028,2:2029}[no])
                        r[ared] = base
                        r[system], r[tech], r[status], r[developer] = 'Jawa Bali','PLTSa', {1:'Pendanaan',2:'Rencana'}[no], 'IPP'
                    row = dict(resource_id=f'R25-{province.replace(" ", "_")}-{no:03}',
                        plant_id='', unit_id='', parent_id='', row_level='planning_resource_or_quota',
                        name=nm, province=province, technology=clean(r[tech]), fuel='',
                        source_system=clean(r[system]), boundary_class='interconnected_candidate' if clean(r[system])=='Jawa Bali' else 'separate_system_candidate',
                        status=clean(r[status]), reporting_organisation='PT PLN (Persero)',
                        developer_class=clean(r[developer]), installed_mw='', dependable_mw='',
                        planned_mw=num(clean(r[cap])), capacity_source_text=clean(r[cap]),
                        cod_re_base=base, cod_ared=clean(r[ared]), commissioning_evidence='projected COD only; not observed commissioning',
                        retirement_evidence='', connection=clean(r[system]),
                        source_id='L6', source_page=page, source_row=no, source_date='2025-05-26 approval',
                        source_url=RUPTL_URL, unresolved='official plant/unit ID; terminal; operating parameters; actual commissioning; costs; retirement',
                        aggregation_rule='separate candidates by scenario; never add to existing fleet automatically')
                    if 'Kuota' in nm or 'Smoothing' in nm:
                        row['row_level']='planning_quota'
                        row['unresolved'] += '; site allocation; potential-list overlap'
                    if '*' in clean(r[cap]):
                        footnotes={'Banten':'replacement of oil/gas steam plant', 'Jawa Barat':'efficiency addition to existing plant without added gas consumption', 'Jawa Timur':'relocation of existing asset'}
                        row['unresolved'] += '; footnote: '+footnotes.get(province,'inspect page-specific capacity footnote')
                    rows.append(row)
        ids = [r['source_row'] for r in rows]
        # Explicit sequence check exposes missed/merged PDF rows rather than hiding them.
        assert len(ids)==len(set(ids)), (province, 'duplicate source rows')
        assert ids == list(range(1,max(ids)+1)), (province, ids)
        for scenario in ['re_base','ared']:
            selected=[r for r in rows if re.fullmatch(r'20\d\d',r['cod_'+scenario])]
            reconciliations.append(dict(definition=f'{province} published candidate list; {scenario}',
                quantity='planned MW including storage/quotas/isolated where listed',
                extracted_sum=round(sum(r['planned_mw'] or 0 for r in selected),6), source_total=published,
                residual=round(sum(r['planned_mw'] or 0 for r in selected)-(published or 0),6),
                interpretation='source total is not assumed scenario-specific; retain residual, blank COD excluded, no forced balancing'))
            # Compare like-for-like with the scenario recap, retaining replacement,
            # relocation and efficiency rows separately in the inventory.
            recaps = {'DKI':(185,185,818,818), 'Banten':(3927,5087,829,830),
                'Jawa Barat':(6836,9817,848,849), 'Jawa Tengah':(2944,7403,880,880),
                'DIY':(50,450,901,901), 'Jawa Timur':(4015,7865,912,913),
                'Bali':(2339,2744,942,943)}
            k = 0 if scenario=='re_base' else 1
            adjusted=[r for r in selected if '*' not in r['capacity_source_text']]
            recap=recaps[province][k]
            value=round(sum(r['planned_mw'] or 0 for r in adjusted),6)
            assert abs(value-recap) < 1, (province,scenario,value,recap)
            reconciliations.append(dict(definition=f'{province} {scenario} scenario recap PDF{recaps[province][k+2]}',
                quantity='MW listed additions excluding explicitly footnoted replacements/efficiency/relocations',
                extracted_sum=value,source_total=recap,residual=round(value-recap,6),
                interpretation='bounded arithmetic bridge, not proof all MW is connected or new nameplate; rounding/source residual retained'))
        planned.extend(rows)
    write('planned_resources.csv', planned)
    assert len(planned)==294
    assert all(r['name'] and r['planned_mw'] is not None for r in planned)
    (OUT / 'planning_table_cells.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')

    seed=json.loads((BASE / 'jamali_existing_resource_evidence.json').read_text())
    existing=[]
    for i,r in enumerate(seed['resources'],1):
        page=r['page']
        row=dict(resource_id=f'EX-{i:03}',plant_id='',unit_id='',parent_id='',row_level=r.get('level','plant_or_complex'),
            name=r['name'],province=r['province'],technology=r['technology'],fuel=r.get('fuel',''),
            boundary_class=r.get('boundary','interconnected_existing'),status='existing in source context (2024); not verified current 2026',
            connection=r['connection'],reporting_organisation=r.get('reporter','PT PLN (Persero)'),
            installed_mw=r.get('installed_mw',''),dependable_mw=r.get('dependable_mw',''),
            capacity_definition=r.get('capacity_definition','not supplied at named-resource level'),
            commissioning_evidence='',retirement_evidence='',source_id=r.get('source_id','L6'),
            source_page=page,source_date='2024 reporting context / 2025 publication',
            source_url=NP_URL if r.get('source_id')=='I2' else RUPTL_URL,
            unresolved=r.get('unresolved','official IDs; unit breakdown; capacities; commissioning/retirement; operator legal entity; detailed fuel specification'),
            aggregation_rule=r.get('rule','partial named-resource evidence; no full-grid total'))
        existing.append(row)
    write('existing_resources.csv',existing)
    # These are electrical systems, not invented individual generators.
    isolated=[dict(system_id=f'ISO-EJ-{i:02}',name=nm,province='Jawa Timur',boundary_class='isolated_excluded',
        source_id='L6',source_page=918,source_url=RUPTL_URL,source_date='2025-05-26 approval',
        installed_mw='',plant_ids='',unresolved='resource list; unit IDs; capacity; time series',rule='exclude from interconnected fleet until dated connection evidence')
        for i,nm in enumerate(seed['east_java_isolated_systems'],1)]
    assert len(isolated)==25
    write('isolated_systems.csv',isolated)
    write('boundary_crosswalk.csv',seed['boundary_crosswalk'])
    write('capacity_observations.csv',seed['capacity_observations'])
    write('reconciliation.csv',reconciliations+seed['reconciliations'])
    # Real local samples; no generic load shape or emissions factor is manufactured.
    monthly=list(csv.DictReader((ROOT/'geothermal_ml_data_research/data/wayang_windu_monthly_main_meter_2018_2021.csv').open()))
    daily=list(csv.DictReader((ROOT/'geothermal_ml_data_research/data/wayang_windu_daily_examples.csv').open()))
    assert len(monthly)==42 and len({r['month'] for r in monthly})==42
    assert len(daily)==len({r['date'] for r in daily})
    write('sample_wayang_windu_monthly.csv',monthly)
    write('sample_wayang_windu_daily.csv',daily)
    # Published annual demand proxy, not coincident interval system load.
    sales=[r for r in csv.DictReader((ROOT/'ruptl_eda/output/ruptl_historical_sales.csv').open()) if r['grid']=='Jamali']
    write('sample_historical_sales.csv',sales)
    write('annual_operating_characteristics.csv',[
        dict(name=n,year=2024,nphr_kcal_per_net_kwh=heat,eaf_percent=eaf,
             source_id='I2',nphr_pdf_page=42 if i<5 else 43,
             eaf_pdf_page=36 if i<5 else 37,source_url=NP_URL,
             limitation='annual reporting-resource average, not incremental heat-rate curve or interval availability')
        for i,(n,heat,eaf) in enumerate([
            ('UP Paiton',2808.25,83.77),('UP Indramayu',2951.33,79.49),
            ('UP Rembang',2914.85,86.61),('UP Pacitan',2857.42,87.89),
            ('UP Tanjung Awar-Awar',2790.36,88.26),('UP Muara Karang',1969.34,94.10)])])
    allrows=existing+planned
    assert len({r['resource_id'] for r in allrows})==len(allrows)
    checks=dict(existing_named_rows=len(existing),planning_rows=len(planned),isolated_systems=len(isolated),
        monthly_sample_rows=len(monthly),daily_sample_rows=len(daily),
        complete_unit_inventory=False,source_hashes_verified=True,duplicate_resource_ids=0,
        planned_sequences_contiguous=True,full_grid_reconciliation='unresolved; partial existing named-resource coverage',
        numerical_mef_pilot_cleared=False)
    (OUT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':
    run()
