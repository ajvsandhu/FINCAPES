"""Reproduce bounded 2024 IPP/other-PLN identity audit; no network or model."""
import csv
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
import fitz

class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.skip+=1
    def handle_endtag(self,tag):
        if tag in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip and data.strip():self.parts.append(data.strip())

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
OUT=BASE/'output/ipp_alias_audit'

def save(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)

def audit():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((BASE/'ipp_alias_manifest.json').read_text())
    sources={s['source_id']:s for s in manifest['inputs']}
    for s in sources.values():
        assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256'],s['path']
    # Scanned decree: manual factual transcription checked against rendered pages,
    # not an assertion that this PDF has extractable machine-readable text.
    decree=fitz.open(ROOT/sources['I4']['path'])
    assert len(decree)==72 and not decree[51].get_text().strip()
    for n in [1,4,51,52]:
        decree[n-1].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(OUT/f'esdm310_page_{n}.png')
    texts={}
    for key in ['I5','I6','I8','I9']:
        parser=TextOnly();parser.feed((ROOT/sources[key]['path']).read_text())
        texts[key]=' '.join(parser.parts)
    assert '660' in texts['I5'] and '3A' in texts['I5'] and 'November 2019' in texts['I5']
    assert '945' in texts['I6'] and '55 MW' in texts['I6']
    assert '15 August 2022' in texts['I9'] and '31 August 2022' in texts['I9']
    (OUT/'html_text_snapshots.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2)+'\n')
    units=[]
    def add(key,site,label,org,reported,capacity_source,commission='',precision='',aliases=''):
        units.append(dict(resource_key=key,site=site,source_unit_label=label,
            official_registry_unit_id='',reporting_organisation=org,technology='PLTU',fuel='coal',
            boundary='interconnected Jamali; RUPTL PDF874 / specific operator connection evidence',
            location='Central Java',membership_anchor='2024-11-28',
            membership_basis='listed in ESDM 310/2024 target rows plus historical operating evidence; not interval availability',
            status='historical unit identity supported; not current dispatch verification',
            source_reported_mw=reported,capacity_basis='source nominal/project capacity; not assigned installed or DMN',
            installed_mw='',dependable_mw='',capacity_source_id=capacity_source,
            capacity_source_url=sources[capacity_source]['url'],
            capacity_source_location={'I8':'item3','I4':'PDF52 row136','I5':'List of Units','I9':'opening paragraphs'}[capacity_source],
            capacity_source_date=sources[capacity_source]['date'],
            membership_source_url=sources['I4']['url'],
            membership_pdf_page=51 if key.startswith('BATANG') else 52,
            commissioned_evidence=commission,commissioning_precision=precision,retirement_evidence='',
            aliases=aliases,source_ids='I4;'+capacity_source,
            unresolved='registry ID; same-date unit installed/DMN; operating observations; retirement',
            sum_rule='identity union only; no mixed-basis capacity total'))
    for n in range(1,5):
        add(f'TJB-U{n}','Tanjung Jati B',f'Unit {n}','PT PLN (Persero) UIK Tanjung Jati B',660,'I8',
            'existing units1–4 in 2017 ESDM fact sheet; no exact COD assigned','existing_before_2017',
            'Tanjung Jati B original units; EX-020')
    for n in [5,6]:
        add(f'TJB-U{n}','Tanjung Jati B',f'Unit {n}','PT Bhumi Jati Power',1000,'I4',
            'project commercial operation September 2022, Kansai page; not individual unit COD','project_month',
            'Jawa 4; EX-025; expansion units5–6')
    for label,mw,cod in [('1',300,'2006-09'),('2',300,'2006-09'),('3',660,'2016-06'),('3A',1000,'2019-11')]:
        add('S2P-U'+label,'Cilacap Sumber Segara Primadaya','Unit '+label,'PT Sumber Segara Primadaya',mw,'I5',
            cod,'month',{'1':'Cilacap original; EX-027','2':'Cilacap original; EX-027',
            '3':'Cilacap Expansion I; EX-022','3A':'Cilacap Expansion II; Jawa 8; EX-023'}[label])
    for n,cod in [(1,'2022-08-15'),(2,'2022-08-31')]:
        add(f'BATANG-U{n}','Batang / Jawa Tengah PPP',f'Unit {n}','PT Bhimasena Power Indonesia',1000,'I9',
            cod,'day','Jawa Tengah PPP; EX-024; distinct from Tanjung Jati B/Jawa4')
    assert len(units)==len({r['resource_key'] for r in units})==12
    save('dated_identity_union.csv',units)
    registry=[
        dict(row=127,pdf_pages='51',name='PLTU Jawa Tengah',organisation='PT Bhimasena Power Indonesia',
             source_capacity_text='PLTU 2x1.000 MW',disposition='target: Batang units1–2'),
        dict(row=131,pdf_pages='51',name='PLTU dan GISTET Adipala',organisation='PT PLN Indonesia Power UBP Adipala; PLN UIT JBT',
             source_capacity_text='PLTU 660 MW; GISTET500kV',disposition='existing IP control; do not append duplicate 660 MW; substation excluded'),
        dict(row=132,pdf_pages='51–52',name='PLTU, GISTET dan GIS Cilacap',organisation='PT Sumber Segara Primadaya',
             source_capacity_text='Unit1 300MW; Unit2 300MW; Ekspansi660MW; EkspansiFaseII Jawa8 1.000MW; GISTET500kV; GIS150kV',
             disposition='target four units; substation entries excluded from generation'),
        dict(row=133,pdf_pages='52',name='PLTG Lomanis',organisation='PT PLN Indonesia Power UBP Semarang',
             source_capacity_text='PLTG2x29MW',disposition='control only; alias/current status relative to IP2024 unresolved; do not add to unit union'),
        dict(row=134,pdf_pages='52',name='PLTA, GI Mrica, Waduk dan Bendungan PB Sudirman',organisation='PT PLN Indonesia Power UBP Mrica; PLN UIT JBT',
             source_capacity_text='PLTA180MW; GI150kV',disposition='Mrica/PB Sudirman name bridge; not full UBP portfolio; no extra plant'),
        dict(row=135,pdf_pages='52',name='PLTGU, GI dan GIS Tambak Lorok',organisation='PT PLN Indonesia Power UBP Semarang; PLN UIT JBT',
             source_capacity_text='PLTGU1.469MW; GI/GIS150kV',disposition='control only; different capacity from IP2024; no forced correction or new resource'),
        dict(row=136,pdf_pages='52',name='PLTU dan GI Tanjung Jati B',organisation='PLN UIK Tanjung Jati B; PT Bhumi Jati Power; PLN UIT JBT',
             source_capacity_text='Unit1&2 1.420MW; Unit3&4 1.420MW; Jawa4 units5&6 2x1.000MW; GI150kV',
             disposition='target six units, separate reporting groups; no allocation of1420MW pair totals to invented unit installed values'),
        dict(row=137,pdf_pages='52',name='PLTU dan GI PLTU Rembang',organisation='PT PLN Nusantara Power UP Rembang; PLN UIT JBT',
             source_capacity_text='PLTU2x315MW; GI150kV',disposition='existing NP control; no duplicate 630MW; substation excluded')]
    for r in registry:r.update(source_id='I4',source_date='2024-11-28',source_url=sources['I4']['url'],basis='security/vital-object register, not a comprehensive operational fleet census')
    save('selected_official_register_rows.csv',registry)
    # Alternative observations stay separate from canonical identities.
    observations=[]
    def obs(group,value,basis,sid,location,date):
        observations.append(dict(group=group,reported_mw=value,capacity_basis=basis,source_id=sid,
            source_location=location,reference_date=date,source_url=sources[sid]['url'],
            rule='alternative observation; not additive; do not infer unspecified gross/net/DMN conversion'))
    obs('TJB units1–4',2811.4,'installed, explicitly labelled','J2','Table1 PDF19; Table21 PDF60','2024 year-end')
    obs('TJB units1–4',2643.8,'Daya Mampu, explicitly labelled','J2','Table1 PDF19; Table22 PDF62','2024 year-end')
    obs('TJB units1–4',2840,'two listed pair capacities1420+1420; basis unspecified','I4','row136 PDF52','2024-11-28')
    obs('TJB units1–4',2640,'4x660; fact-sheet nominal capacity, not labelled DMN','I8','item3','2017-08-31')
    obs('TJB units5–6 / Jawa4',2000,'2x1000; register/project capacity, basis unspecified','I4','row136 PDF52','2024-11-28')
    obs('TJB units5–6 / Jawa4',2140,'2x1070; sponsor page capacity, basis unspecified','I7','Capacity / Project Overview','undated, retrieved2026-11-11')
    obs('TJB units5–6 / Jawa4',535,'25% equity-equivalent capacity; exclude from physical resource totals','I7','Equity portion','undated, retrieved2026-11-11')
    obs('Cilacap S2P four units',2260,'operator nominal capacity300+300+660+1000','I5','Company Profile / List of Units','undated retrospective, retrieved2026-11-11')
    obs('Cilacap ExpansionII / Jawa8',1000,'total capacity before stated plant use','I6','press release paragraphs1,3','2020-02-17')
    obs('Cilacap ExpansionII / Jawa8',55,'plant own-use capacity; not another generator','I6','paragraph3','2020-02-17')
    obs('Cilacap ExpansionII / Jawa8',945,'capacity supplied to PLN after stated own use; not annual DMN measurement','I6','paragraph3','2020-02-17')
    obs('Batang units1–2',2000,'2x1000 project capacity, basis unspecified','I4','row127 PDF51','2024-11-28')
    save('capacity_observations.csv',observations)
    crosswalk=[]
    for ex,alias,keys,rule in [
        ('EX-020','Tanjung Jati B',[f'TJB-U{n}' for n in range(1,5)],'RUPTL lists Jawa4 separately; original PLN reporting group mapped to units1–4'),
        ('EX-025','Jawa4',['TJB-U5','TJB-U6'],'same units as TJB expansion5–6; no additional Jawa4 pseudo-plant'),
        ('EX-027','Cilacap',['S2P-U1','S2P-U2'],'original pair distinct from expansionI and expansionII; whole-site name sometimes broader'),
        ('EX-022','Cilacap Exp',['S2P-U3'],'RUPTL separate Jawa8 plus ESDM expansionI660MW bridge; generic expansion wording alone remains broad'),
        ('EX-023','Jawa8',['S2P-U3A'],'ESDM ExpansionII alias plus operator unit3A name/capacity/COD; exact generic registry ID missing'),
        ('EX-024','Jawa Tengah (PPP)',['BATANG-U1','BATANG-U2'],'BPI/Batang separate site and company from BJP/Jawa4'),
    ]:
        crosswalk.append(dict(existing_evidence_id=ex,alias=alias,canonical_unit_keys=';'.join(keys),
            evidence='I4 rows127/132/136; I5; I6; I8; I9; RUPTL PDF874',match_rule=rule,
            reference_date='2024-11-28 membership anchor',official_registry_id_status='not acquired'))
    assert len({k for r in crosswalk for k in r['canonical_unit_keys'].split(';')})==12
    assert sum(len(r['canonical_unit_keys'].split(';')) for r in crosswalk)==12
    save('alias_crosswalk.csv',crosswalk)
    checks=[dict(check='Cilacap operator four-unit nominal total',left=300+300+660+1000,right=2260,residual=0,basis='like-for-like source nominal total, not a DMN sum'),
        dict(check='Jawa8 total minus stated own use',left=1000-55,right=945,residual=0,basis='explicit 2020 release bridge; no annual DMN claim'),
        dict(check='Cilacap geographical group includes separate Adipala',left=2260+660,right=2920,residual=0,basis='2020 release geographic total; not S2P portfolio alone'),
        dict(check='TJB register minus2024 installed',left=2840,right=2811.4,residual=28.6,basis='UNRESOLVED source-definition difference; not inferred own-use'),
        dict(check='Jawa4 sponsor minus register capacity',left=2140,right=2000,residual=140,basis='UNRESOLVED capacity definition; no verified conversion'),
        dict(check='TJB installed minus DayaMampu',left=2811.4,right=2643.8,residual=167.6,basis='distinct labelled quantities; not assigned to losses or own-use')]
    save('reconciliation.csv',checks)
    # Parse existing official annual row, rather than trusting the transcription.
    stats=fitz.open(ROOT/sources['J2']['path'])
    selected={str(n):stats[n-1].get_text(sort=True) for n in [19,58,60,62]}
    row=next(l for l in selected['19'].splitlines() if 'UIK Tanjung Jati B' in l)
    assert '2.811,40' in row and '2.643,80' in row
    (OUT/'pln_annual_source_rows.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    summary=dict(membership_anchor='2024-11-28',canonical_unit_labels=12,physical_sites=3,
        official_register_target_rows=3,selected_register_control_rows=5,alias_crosswalk_rows=6,
        registry_identifiers_acquired=0,mixed_basis_total_blocked=True,
        target_same_source_annual_installed_mw=2811.4,target_same_source_annual_daya_mampu_mw=2643.8,
        annual_capacity_reference='2024 year-end; not assigned to November28 without further evidence',
        unit_labels_outside_verified_annual_reporting_group=8,
        unit_level_installed_DMN_pairs_acquired=0,
        numerical_mef_cleared=False,full_grid_coverage_percent=None,
        general_warning='dated partial identity union, not complete 2024 Jamali fleet; no within-year retirement/availability inference')
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,2.8))
    fig.subplots_adjust(left=.06,right=.97,top=.65,bottom=.30)
    ax.barh([0],[945],color='#176b70',height=.6)
    ax.barh([0],[55],left=[945],color='#c08b32',height=.6)
    ax.text(472.5,0,'945 MW supplied to PLN',ha='center',va='center',color='white',fontsize=12)
    ax.annotate('55 MW plant use',xy=(972.5,.3),xytext=(780,.8),ha='center',
                arrowprops=dict(arrowstyle='-',color='#65532d'),fontsize=10)
    ax.set_xlim(0,1000);ax.set_ylim(-.6,1);ax.axis('off')
    fig.suptitle('Jawa 8 / Cilacap Expansion II: the stated capacity bridge',x=.06,ha='left',fontsize=13)
    fig.text(.06,.76,'1,000 MW total capacity = 945 MW to PLN + 55 MW for plant use',fontsize=11)
    fig.text(.06,.12,'Source: ESDM press release, 17 February 2020. This is a source-stated capacity bridge,\nnot measured 2024 dispatch, annual dependable capacity or an emissions estimate.',fontsize=9)
    fig.savefig(OUT/'jawa8_capacity_bridge.png',dpi=180,facecolor='white');plt.close(fig)
    (OUT/'jawa8_capacity_bridge.html').write_text('<!doctype html><html><body><img style="width:100%;height:auto" alt="Jawa8 source-stated capacity bridge" src="'+str(OUT/'jawa8_capacity_bridge.png')+'"/></body></html>')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':audit()
