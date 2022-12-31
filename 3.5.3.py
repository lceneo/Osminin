
import sqlite3
import pandas as pd

connection = sqlite3.connect('project_vacancy.db')
jobs = input('Введите название вакансии: ')
dataframe_f = pd.read_sql("""select strftime('%Y',published_at) as date, round(avg(salary)) as avg_salary 
                        from vacancies 
                        group by strftime('%Y',published_at)""", connection)
dataframe_s = pd.read_sql("""select strftime('%Y',published_at) as date, count(salary) as count 
                        from vacancies 
                        group by strftime('%Y',published_at)""", connection)
dataframe_t = pd.read_sql(f"""select strftime('%Y',published_at) as date, round(avg(salary)) as avg_salary 
                        from vacancies
                        where name like '%{jobs}%' 
                        group by strftime('%Y',published_at)""", connection)
dataframe_f = pd.read_sql(f"""select strftime('%Y',published_at) as date, count(salary) as count 
                        from vacancies
                        where name like '%{jobs}%' 
                        group by strftime('%Y',published_at)""", connection)
dataframe_fifth = pd.read_sql("""select area_name, avg from
                        (select area_name, round(avg(salary)) as avg, count(salary) as count
                        from vacancies
                        group by area_name
                        order by avg desc)
                    where count > (select count(*) from vacancies) * 0.01
                    limit 10""", connection)
dataframe_s = pd.read_sql("""select area_name,
                        round(cast(count as real) / (select count(*) from vacancies), 4) as percent from
                        (select area_name, count(salary) as count
                        from vacancies
                        group by area_name
                        order by count desc)
                        limit 10""", connection)
pd.set_option('expand_frame_repr', False)
print('Динамика уровня зарплат по годам \n', dataframe_f)
print('Динамика количества вакансий по годам \n', dataframe_s)
print('Динамика уровня зарплат по годам для выбранной профессии \n', dataframe_t)
print('Динамика количества вакансий по годам для выбранной профессии \n', dataframe_f)
print('Уровень зарплат по городам (в порядке убывания) - только первые 10 значений \n', dataframe_fifth)
print('Доля вакансий по городам (в порядке убывания) - только первые 10 значений \n', dataframe_s)
