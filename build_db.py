#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import psycopg2
import psycopg2.extras
import json


# ## Original data

# In[12]:


csv_path = './species_data/SNIBEjemplares_20240520_142214.zip'

conn = psycopg2.connect(
    dbname='ep2_2',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

table_name = 'ep2_2_schema.original'
chunksize = 1000000

for chunk in pd.read_csv(csv_path, chunksize=chunksize):
    
    chunk['ejemplarfosil'] =  chunk['ejemplarfosil'].fillna('NO')
    chunk['ejemplarfosil'] =  chunk['ejemplarfosil'].apply(lambda x: False if x == 'NO' else True)
    chunk['geoportal'] =  chunk['geoportal'].apply(lambda x: bool(x))
    chunk = chunk[~(chunk['longitud'].isna()) | ~(chunk['longitud'].isna())]
    #chunk['the_geom'] = pd.Series(['ST_SetSRID(ST_Point(longitud, latitud), 4326)' for i in range(chunk.shape[0])])
    
    with conn.cursor() as cursor:
        columns = ','.join([col for col in chunk.columns])
        placeholders = ','.join(['%s' for _ in range(len(chunk.columns))])
        sql = f"INSERT INTO {table_name}({columns}) VALUES ({placeholders})"
        data = [tuple(row) for row in chunk.values]
        cursor.executemany(sql, data)
        conn.commit()

with conn.cursor() as cursor:
    sql = f"UPDATE ep2_2_schema.original SET the_geom=ST_SetSRID(ST_Point(longitud, latitud), 4326)"
    cursor.execute(sql)
    conn.commit()

conn.close()


# ### Variables

# In[13]:


conn = psycopg2.connect(
    dbname='ep2_2',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    sql = f"SELECT distinct reinovalido, phylumdivisionvalido, clasevalida,\
    ordenvalido, familiavalida, generovalido, especievalida FROM ep2_2_schema.original"
    cursor.execute(sql)
    variables = cursor.fetchall()
    
    sql = f"INSERT INTO ep2_2_schema.variable(\"values\") VALUES (%s::json)"
    data = [(json.dumps(v),) for v in variables]
    cursor.executemany(sql, data)
    conn.commit()

conn.close()


# ## Occurrences

# ### Occurrences for ind ensemble

# In[15]:


conn = psycopg2.connect(
    dbname='ep2_2',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    sql = f"SELECT * FROM ep2_2_schema.variable"
    cursor.execute(sql)
    variables = cursor.fetchall()
    for v in variables:
        #print(v['id'])
        where_clause = 'and '.join([k+'=\''+v['values'][k]+'\' ' for k in v['values'].keys()])
        sql = f"SELECT id FROM ep2_2_schema.original WHERE {where_clause}"
        cursor.execute(sql)
        occs = cursor.fetchall()
        
        sql = f"INSERT INTO ep2_2_schema.occurrence_ensemble_ind VALUES(%s, %s)"
        data = [(occ['id'], v['id']) for occ in occs]
        cursor.executemany(sql, data)
        conn.commit()

conn.close()


# ### Occurrences for 16k ensemble

# In[2]:


conn = psycopg2.connect(
    dbname='ep2_1',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    sql = f"INSERT INTO ep2_2_schema.occurrence_ensemble_16k \
        select m.cve::integer as cell_id, o.variable_id \
        from ep2_2_schema.occurrence_ensemble_ind as o \
        left join ep2_2_schema.original as s on o.cell_id=s.id \
        left join public.mesh_16km as m on st_intersects(s.the_geom, m.geometry)\
        WHERE cell_id is not null;"
    cursor.execute(sql)
    conn.commit()

conn.close()


# ## Summaries

# ### Summary for ind ensemble

# In[5]:


conn = psycopg2.connect(
    dbname='ep2_2',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    sql = 'INSERT INTO ep2_2_schema.summary_ensemble_ind \
        SELECT variable_id, \
            array_agg(DISTINCT cell_id) AS cells, \
            array_length(array_agg(DISTINCT cell_id), 1) AS occs \
        FROM ep2_2_schema.occurrence_ensemble_ind \
        GROUP BY variable_id;'
    cursor.execute(sql)
    conn.commit()

conn.close()


# ### Summary for 16k ensemble

# In[4]:


conn = psycopg2.connect(
    dbname='ep2_2',
    user='postgres',
    password='!37JzLg+9M2RAu72',
    host='10.90.0.35',
    port=5433
)

with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
    sql = 'INSERT INTO ep2_2_schema.summary_ensemble_16k \
        SELECT variable_id, \
            array_agg(DISTINCT cell_id) AS cells, \
            array_length(array_agg(DISTINCT cell_id), 1) AS occs \
        FROM ep2_2_schema.occurrence_ensemble_16k \
        GROUP BY variable_id;'
    cursor.execute(sql)
    conn.commit()

conn.close()


# In[ ]:




