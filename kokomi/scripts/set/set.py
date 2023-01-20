import json
import os
import sys
import sqlite3
import httpx

file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class bind():
    def server_url(self, server: str) -> str:
        '''Return the domain name of the server's website'''
        url_list = {
            'asia': 'http://vortex.worldofwarships.asia',
            'eu': 'http://vortex.worldofwarships.eu',
            'na': 'http://vortex.worldofwarships.com',
            'ru': 'http://vortex.korabli.su',
            'cn': 'http://vortex.wowsgame.cn'
        }
        return url_list[server]

    async def set_id(self, user_qqid, game_id, server):
        async with httpx.AsyncClient() as client:
            try:
                url = self.server_url(
                    server) + '/api/accounts/search/{}/?limit=50'.format(game_id.lower())
                res = await client.get(url, timeout=3)
                if res.status_code != 200:
                    return {'status': 'error', 'message': 'NETWORK ERROR', 'error': 'Status Code:'+str(res.status_code)}
                result = res.json()
            except:
                return {'status': 'error', 'message': 'NETWORK ERROR'}
        if result["status"] == "error":
            return {'status': 'error', 'message': 'NETWORK ERROR'}
        if result['data'] == []:
            return {'status': 'error', 'message': 'No Result'}
        if result['data'][0]['name'].lower() != game_id.lower():
            return {'status': 'error', 'message': 'No Result'}
        else:
            accountid = result['data'][0]['spa_id']

        conn = sqlite3.connect(os.path.join(file_path, 'data', 'userid.db'))
        c = conn.cursor()
        cursor = c.execute(
            "SELECT QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2  from userid")
        for row in cursor:
            if row[0] == int(user_qqid):
                old_accid = row[1]
                statements = "UPDATE userid set TIME = 0 where QQID=" + \
                    str(user_qqid)
                c.execute(statements)
                statements = "UPDATE userid set ACCID = " + \
                    str(accountid)+" where QQID="+str(user_qqid)
                c.execute(statements)
                statements = "UPDATE userid set SERVER = '" + \
                    str(server)+"' where QQID="+str(user_qqid)
                c.execute(statements)
                conn2 = sqlite3.connect(os.path.join(
                    file_path, 'data', 'accountid.db'))
                c2 = conn2.cursor()
                user = False
                try:
                    c2.execute(
                        f"INSERT INTO accid (ACCID, TIME, SERVER) VALUES ({accountid},0,'{server}')")
                except:
                    user = True
                    continue
                conn2.commit()
                conn2.close()
                break
        if conn.total_changes == 3:
            conn.commit()
            conn.close()
            return {'status': 'ok', 'message': 'Change Id', 'data': [old_accid, accountid], 'new_user': user}
        else:
            statements = "INSERT INTO userid (QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2) VALUES (" + str(
                user_qqid) + "," + str(accountid) + ", 1, 'cn', 0, '"+str(server)+"', '0', '0' )"
            c.execute(statements)
            conn.commit()
            conn.close()
            conn2 = sqlite3.connect(os.path.join(
                file_path, 'data', 'accountid.db'))
            c2 = conn2.cursor()
            user = False
            try:
                c2.execute(
                    f"INSERT INTO accid (ACCID, TIME, SERVER) VALUES ({accountid},0,'{server}')")
            except:
                user = True
            conn2.commit()
            conn2.close()
            return {'status': 'ok', 'message': 'Bind Id', 'new_user': user}
