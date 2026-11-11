"""Offline audit of official PLN Indonesia Power 2024 roster; no model fit."""
import csv
import hashlib
import json
import re
from pathlib import Path
import fitz

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
OUT = BASE/'output/ip_roster_audit'
URL = 'https://ipstore.plnindonesiapower.co.id:1996/statisticreport2024/files/downloads/Laporan_Statistik_IP_2024.pdf'
RUPTL = 'https://gatrik.esdm.go.id/gatrik/gatrik-api/storage/migrasi/download_index/files/b967d-ruptl-pln-2025-2034-pub-.pdf'

def number(s):
    return float(s.replace('.','').replace(',','.'))

def save(name, rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)

def words(page):
    result=[]
    for w in page.get_text('words'):
        r=fitz.Rect(w[:4])*page.rotation_matrix
        result.append(dict(x=r.x0,y=r.y0,cx=(r.x0+r.x1)/2,text=w[4]))
    return result

def audit():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((BASE/'ip_roster_manifest.json').read_text())
    for item in manifest['inputs']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    pdf=fitz.open(BASE/'raw/pln_ip_statistics_2024.pdf')
    assert len(pdf)==76
    pages={str(n):pdf[n-1].get_text(sort=True) for n in manifest['inspected_ip_pdf_pages']}
    (OUT/'page_text_snapshots.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
    plants=[]; machines=[];raw=[]; parent=''
    java_groups=['Suralaya','Priok','Saguling','Semarang','Mrica','Grati','Bali',
        'Banten 1 Suralaya','Banten 2 Labuan','Banten 3 Lontar',
        'Jawa Barat 2 Pelabuhan Ratu','Jawa Tengah 2 Adipala','Cilegon','Jatigede']
    # Table 13 is landscape text printed on portrait pages. Transform word
    # coordinates; do not rewrite or rotate the archived source binary.
    for n in range(34,40):
        page=pdf[n-1];page.set_rotation(90)
        ws=words(page)
        ymin=130 if n%2==0 else 150
        headers=[w for w in ws if 195<w['x']<715 and w['y']<ymin and w['text'].isdigit() and 1<=int(w['text'])<=21]
        assert len(headers)==21,(n,headers)
        relevant=[w for w in ws if 70<w['x']<775 and ymin<w['y']<555]
        anchors=sorted([w for w in relevant if w['x']<85 and
            (w['text'].startswith('PLT') or w['text']=='UBP/GBU')],key=lambda w:w['y'])
        for i,a in enumerate(anchors):
            stop=anchors[i+1]['y']-1 if i+1<len(anchors) else 555
            band=sorted([w for w in relevant if a['y']-1<w['y']<stop],key=lambda w:(round(w['y']/3),w['x']))
            # Header labels sometimes span two lines. Numeric values are on
            # the same physical line as plant technology labels.
            if a['text']=='UBP/GBU':
                parent=' '.join(w['text'] for w in band if w['x']<195 and w['text']!='UBP/GBU')
                raw.append(dict(pdf_page=n,kind='parent',parent=parent,words=band))
                continue
            line=sorted([w for w in band if abs(w['y']-a['y'])<2.5],key=lambda w:w['x'])
            tech=' '.join(w['text'] for w in line if w['x']<138)
            name=' '.join(w['text'] for w in line if 138<=w['x']<195)
            values=[w for w in line if 195<=w['x']<715]
            count=[w['text'] for w in line if 715<=w['x']<738]
            total=[w['text'] for w in line if 738<=w['x']<775]
            assert name and len(count)==len(total)==1,(n,line)
            # Boundary is assigned to resources, never to the UBP name alone.
            if parent=='Kamojang':
                cls='connected_in_scope' if name in ['Kamojang','Gunung Salak','Darajad'] else 'outside_jamali_excluded'
                evidence='RUPTL p842 PLTP Salak; p843 existing West Java geothermal; other named fields outside Java'
            elif parent in java_groups:
                cls='connected_in_scope'
                evidence={'Suralaya':'RUPTL p824 500 kV','Priok':'RUPTL p812 150/500 kV context',
                    'Saguling':'RUPTL p841 Saguling 500 kV; smaller hydro in West Java aggregate',
                    'Semarang':'RUPTL p874 Tambak Lorok 150 kV',
                    'Mrica':'RUPTL p874 Mrica and distributed hydro; constituent terminal allocation unverified',
                    'Grati':'RUPTL p905 150/500 kV','Bali':'RUPTL p938 interconnected Bali; p939 separate Tiga Nusa',
                    'Banten 1 Suralaya':'RUPTL p824 Suralaya 1–8 500 kV',
                    'Banten 2 Labuan':'RUPTL p824 150 kV','Banten 3 Lontar':'RUPTL p824 150 kV',
                    'Jawa Barat 2 Pelabuhan Ratu':'RUPTL p841 150 kV',
                    'Jawa Tengah 2 Adipala':'RUPTL p874 500 kV','Cilegon':'RUPTL p824 150 kV',
                    'Jatigede':'RUPTL p849–850 planning; dated existing-fleet membership unresolved'}.get(parent,'')
                if parent in ['Saguling','Mrica'] and name not in ['Saguling','PB. Sudirman']:
                    cls='boundary_unresolved'
                if parent=='Jatigede':
                    cls='boundary_unresolved'
                if name=='Karimun Jawa' or name.startswith('Nusa Penida'):
                    cls='isolated_excluded';evidence='RUPTL p882 Karimunjawa isolated / p939 Tiga Nusa separate system label; terminal/date bridge unresolved'
            else:
                cls='outside_jamali_excluded';evidence='outside-Jamali business-unit geography; source Table13'
            role='owned_or_ownership_unresolved'
            if '*' in name:
                role='OM_flagged_not_owned'
            plant_id=f'I3-P{n}-{len(plants)+1:03}'
            cap=number(total[0]); components=round(sum(number(w['text']) for w in values),6)
            plant=dict(evidence_id=plant_id,reporting_unit=parent,plant_name=name,technology=tech,
                installed_mw=cap,source_machine_count=int(count[0]),observed_machine_cells=len(values),
                machine_cell_sum_mw=components,component_residual_mw=round(components-cap,6),
                boundary_class=cls,boundary_evidence=evidence,ownership_role=role,
                reporting_organisation='PT PLN Indonesia Power',reporting_year=2024,
                source_id='I3',source_table=13,source_pdf_page=n,source_url=URL,
                official_plant_id='',dependable_mw='',commissioning_date='',retirement_date='',
                unresolved='official IDs; terminal mapping; commissioning/retirement; source count/cell conflicts retained',
                aggregation_rule='plant total is control; never add parent totals and machine rows')
            plants.append(plant)
            for col,w in enumerate(values,1):
                # Table heading is local machine-column numbering. It is not
                # necessarily a station-wide identifier or a gas/steam train.
                machine=dict(parent_evidence_id=plant_id,evidence_id=f'{plant_id}-C{col:02}',
                    plant_name=name,reporting_unit=parent,source_local_column=int(min(headers,key=lambda h:abs(h['cx']-w['cx']))['text']),
                    installed_mw=number(w['text']),source_value=w['text'],boundary_class=cls,
                    official_unit_id='',source_pdf_page=n,source_table=13,source_url=URL,
                    usability='hold if source count or sum conflicts; local column is not official unit ID')
                machines.append(machine)
            raw.append(dict(pdf_page=n,kind='plant',parent=parent,words=line))
    save('plant_roster.csv',plants);save('machine_cells.csv',machines)
    (OUT/'positioned_source_rows.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
    # Table 9 owned-capacity controls; values transcribed from pp30–31.
    owned={'Suralaya':3400,'Priok':2947,'Saguling':798.36,'Kamojang':567,
        'Semarang':2084.05,'Mrica':333.78,'Grati':1258.58,'Bali':854.10,
        'Banten 1 Suralaya':625,'Banten 2 Labuan':600,'Banten 3 Lontar':945,
        'Jawa Barat 2 Pelabuhan Ratu':1050,'Jawa Tengah 2 Adipala':660,
        'Pangkalan Susu':880,'Cilegon':740,'Barru':100,'Sanggau':14,'Sintang':21,
        'Berau':19,'Labuhan Angin':230,'Asam-Asam':260,'Teluk Sirih':245,
        'Ombilin':221,'Singkawang':100,'Mahakam':418.11,'Keramasan':332.01,
        'Barito':149.26,'Tello':130.57,'Kepulauan Riau':36.37,'Bengkulu':236.32,
        'Jambi':157.03,'Bukittinggi':253.50,'Papua Maluku':177.46}
    assert abs(sum(owned.values())-20843.51)<0.011
    controls=[]
    for group,mw in owned.items():
        children=[r for r in plants if r['reporting_unit']==group]
        total=round(sum(r['installed_mw'] for r in children),6)
        controls.append(dict(reporting_unit=group,owned_table9_mw=mw,table9_pdf_page=30 if group not in ['Jambi','Bukittinggi','Papua Maluku'] else 31,
            extracted_table13_child_mw=total,child_minus_owned_mw=round(total-mw,6),
            interpretation='Table13 includes O&M; Table9 is owned; preserve residual and use Table11 controls',source_url=URL))
    save('ownership_controls.csv',controls)
    # Explicit alias/parent crosswalk; source keys do not invent official IDs.
    aliases=[
        ('EX-008','Suralaya 1-8',['Suralaya 1-4','Suralaya 5-7','Suralaya 8'],4025,'RUPTL p824','exact source-capacity group bridge; keep LBE separate'),
        ('EX-002','Tanjung Priok',['Priok'],None,'RUPTL p812','source name match; Priok business-unit total also contains Senayan'),
        ('EX-003','Senayan',['Senayan'],105.3,'RUPTL p812–813','child of Priok reporting unit; do not add to parent'),
        ('EX-005','Cilegon',['Cilegon'],None,'RUPTL p824–825','740 MW IP installed; 739 MW RUPTL aggregate PLTGU; not silently equalised'),
        ('EX-006','Labuan',['Labuan'],600,'RUPTL p824','named-resource match; installed, not dependable'),
        ('EX-007','Lontar',['Lontar 1-3','Lontar 4*'],1260,'RUPTL p824','945 MW owned + 315 MW O&M; do not add 1260 reporting profile to these children'),
        ('EX-013','Saguling',['Saguling'],700.72,'RUPTL p841','dam plant differs from 798.36 MW reporting portfolio; other hydro kept separately'),
        ('EX-018','Pelabuhan Ratu',['Pelabuhan Ratu'],1050,'RUPTL p841','owned row; historical O&M rows in earlier years must not be added'),
        ('EX-019','Salak',['Gunung Salak'],180,'RUPTL p842','IP three-machine group only; not all Salak geothermal capacity or future Salak7/binary candidates'),
        ('EX-021','Adipala',['Adipala'],660,'RUPTL p874','source name bridge'),
        ('EX-026','Tambak Lorok',['Tambak Lorok'],2079.65,'RUPTL p874','CCPP and steam rows both retained; Semarang portfolio additionally includes isolated Karimun Jawa'),
        ('EX-029','Mrica',['PB. Sudirman'],180.9,'RUPTL p874','probable plant-name bridge; official ID unresolved; not full Mrica business portfolio'),
        ('EX-032','Grati',['Grati Blok 1','Grati Blok 2','Grati Blok 3'],1258.58,'RUPTL p905','plant-total bridge; block1 machine inconsistency retained'),
    ]
    crosswalk=[]
    for ex,alias,names,expected,ref,note in aliases:
        matched=[r for r in plants if r['plant_name'] in names]
        amount=round(sum(r['installed_mw'] for r in matched),6)
        if expected is not None:assert abs(amount-expected)<0.011,(alias,amount,expected)
        crosswalk.append(dict(existing_evidence_id=ex,existing_alias=alias,
            roster_evidence_ids=';'.join(r['evidence_id'] for r in matched),
            roster_names=';'.join(r['plant_name'] for r in matched),roster_installed_mw=amount,
            source_reference=ref,source_url=URL,boundary_source_url=RUPTL,match_limit=note))
    save('alias_crosswalk.csv',crosswalk)
    # Roster-wide controls are independent of electrical classification.
    total_table13=round(sum(r['installed_mw'] for r in plants),6)
    comparison=[dict(definition='Table9 owned unit rows versus published national installed total',
        extracted_mw=round(sum(owned.values()),6),source_control_mw=20843.51,residual_mw=round(sum(owned.values())-20843.51,6),source_pages='30–31'),
        dict(definition='Table13 all child plant totals versus Table9 owned + Table11 O&M',
        extracted_mw=total_table13,source_control_mw=round(20843.51+1058.39,6),
        residual_mw=round(total_table13-20843.51-1058.39,6),source_pages='30–39'),
        dict(definition='Table13 Lontar owned and O&M bridge',extracted_mw=1260,
        source_control_mw=945+315,residual_mw=0,source_pages='30,32,36'),
        dict(definition='RUPTL Suralaya1–8 bridge',extracted_mw=4025,source_control_mw=4025,residual_mw=0,source_pages='I3:34,36; L6:824')]
    assert abs(comparison[1]['residual_mw'])<0.05
    save('capacity_reconciliation.csv',comparison)
    totals={c:round(sum(r['installed_mw'] for r in plants if r['boundary_class']==c),6)
        for c in ['connected_in_scope','boundary_unresolved','isolated_excluded','outside_jamali_excluded']}
    conflicts=[r for r in plants if abs(r['component_residual_mw'])>0.011 or r['source_machine_count']!=r['observed_machine_cells']]
    save('source_conflicts.csv',conflicts)
    summary=dict(plants=len(plants),machine_cells=len(machines),boundary_capacity_mw=totals,
        owned_national_control_mw=round(sum(owned.values()),6),source_conflict_rows=len(conflicts),
        all_roster_plant_total_mw=total_table13,alias_crosswalk_rows=len(crosswalk),
        reported_machine_count=sum(r['source_machine_count'] for r in plants),
        connected_plant_total_with_machine_conflict_mw=round(sum(r['installed_mw'] for r in conflicts if r['boundary_class']=='connected_in_scope'),6),
        ruptl_2025_installed_benchmark_mw=49616,ruptl_2025_dmn_benchmark_mw=46867,
        benchmark_comparison='not a coverage percentage: reporting year, ownership, scope and dependable/installed bases differ',
        compatible_interval_operating_package=False,numerical_mef_cleared=False)
    assert len({m['evidence_id'] for m in machines})==len(machines)
    for plant in plants:
        cols=[m['source_local_column'] for m in machines if m['parent_evidence_id']==plant['evidence_id']]
        assert len(cols)==len(set(cols)),plant['plant_name']
    assert len(plants)==142 and len(machines)==476
    assert abs(sum(totals.values())-total_table13)<0.001
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels=['Mapped to main Jamali grid','Boundary or dated membership unresolved',
            'Isolated systems excluded','Outside Jamali excluded']
    values=list(totals.values())
    fig,ax=plt.subplots(figsize=(10,4.2))
    fig.subplots_adjust(left=.40,right=.92,top=.80,bottom=.21)
    bars=ax.barh(labels,values,color=['#176b70','#b67e21','#728296','#a5b1bd'])
    ax.invert_yaxis();ax.set_xlim(0,19000);ax.set_xlabel('Published plant totals (MW installed)')
    ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
    for b,v in zip(bars,values):ax.text(v+160,b.get_y()+b.get_height()/2,f'{v:,.2f}',va='center',fontsize=10)
    fig.suptitle('Boundary classification of the audited PLN Indonesia Power roster',fontsize=13,x=.05,ha='left')
    fig.text(.05,.87,'2024 source context; owned and O&M resources. This is not the whole Jamali fleet.',fontsize=10)
    fig.text(.05,.05,'Plant totals are controls; machine conflicts remain. No coverage percentage or MEF is inferred.\nSource: PLN Indonesia Power, Statistics 2024, Table 13; RUPTL Annex B boundary checks.',fontsize=9)
    fig.savefig(OUT/'roster_boundary_coverage.png',dpi=180,facecolor='white');plt.close(fig)
    html='''<!doctype html><html><body><img alt="Boundary classification of audited IP roster, not full Jamali coverage" style="width:100%;height:auto" src="'''+str(OUT/'roster_boundary_coverage.png')+'''"/></body></html>'''
    (OUT/'roster_boundary_coverage.html').write_text(html)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':audit()
