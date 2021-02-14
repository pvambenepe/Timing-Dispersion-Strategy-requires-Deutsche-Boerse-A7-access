from SetUp import *
# from GitImport import *
from DateAndTime import DateAndTime

# try to import something from it
from DateAndTime import DateAndTime

DT = DateAndTime(from_date, until_date, force_matu=chosen_matu)
DTi = DateAndTime(from_date, until_date, force_matu=chosen_matu, ital_rule=True)

owner = 'pierrev'
proxies = {
    "http": "",  # Enter http Proxy if needed",
    "https": ""  # Enter https Proxy if needed",
}

API_TOKEN = "Bearer " + "eyJraWQiOiIxNjljMzM2OWE1ZGI5ZTc3NjcwMmE2NThiOTlhYTg4ODE3MDU2NzFhIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhdWQiOiJhNy1hcGkiLCJzdWIiOiIwNzdlM2EyYy01ODkwLTRlYjMtOTkwMi1hMTI0ODJmZTk0ZDciLCJ0b2tlbl91c2UiOiJhcGkiLCJhdXRoX3RpbWUiOjE2MTIzMDY5ODIsImlzcyI6Imh0dHBzOi8vYTctdG9rZW4tc2VydmljZS5kZXV0c2NoZS1ib2Vyc2UuY29tIiwiZ3JvdXBzIjpbImE3LXByb2QtdXNlciJdLCJjb21wYW55IjoiVU5LTk9XTiIsImV4cCI6MTYxNzA2MjQwMCwiaWF0IjoxNjEyMzA2OTgyLCJ1c2VybmFtZSI6InBpZXJyZXYifQ.GLoYn0kxVC310luO2HC65sLmN9-q315rNw-5GphQNXO5DECppNOSzO0BRwn44tvBRrTQJNd_aYX9IjHephxAhpsyIESDlqVX4Poy2F6CDetFdNPtvbf4dpjR6Gc6Ca6zTQrRLwoho_NRPFH_oDmk6lEBAF22NPm_0bRrIlNqX9E0uVUkEL993Tqrcc37NLYdfLymCbGU3qQXpmBMu4uthRnwGgK5B9BBmXg7QqNUjgVnVMGKUO9p6sLhOP7ITl0GwvM4Vo8Uoz022LykitCtRJMEUpmCooXRfQStz0ajOSJluvCKxeawYTL7rzeira40MxjA-4DXOdHmNyJ_rmbBXw"

# algo = 'minsize_level_tb'
# algo = 'top_level'
algo = 'minsize_level_fast'
min_lots = 1

# filter settings to speed up the process
# for 1 year maturity option with an adjustment in sqrt(T)
moneyness_range_call = (-0.025, 0.15)
moneyness_range_put = (-0.15, 0.025)


def get_quotes(opt):
    if opt['PutOrCall'] == 'S':
        market = 'XETR'
    else:
        market = 'XEUR'

    url = 'https://a7.deutsche-boerse.com/api/v1/algo/{}/{}/'.format(owner, algo)
    url = url + "run?marketId={}&date={}&marketSegmentId={}&securityId={}&from_h=9&from_m=10&&min_lots={}&to_h=17&to_m=25&ts_step=120".format(
        market, reference_date, opt['SegmentID'], opt['SecurityID'], min_lots)

    r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
    res = r.json()

    if type(res) == list:
        df_opt = pd.DataFrame.from_dict(res[0]['series'][0]['content'])
        df_opt.ts = df_opt.ts.astype(np.int64)
        df_opt.ts = pd.to_datetime(df_opt.ts)
        df_opt.set_index('ts', inplace=True)

        df_opt[selected_fields_desc] = opt[selected_fields_desc]
        return (df_opt)


def retrieve_instruments_from_A7():

    global res_u, res_f, res_i
    global segmentIDudl, segmentIDfut, segmentIDopt, security
    global matu_list_Stk, matu_list_Fut, matu_list_Opt

    # stock
    if (udl_p not in index_list) and (udl_p[4] != 'no stock on Xetra'):
        lst_ms = np.array([x['MarketSegment'] for x in res_gu['MarketSegments']])
        indx = np.where(lst_ms == isin)[0][0]
        segmentIDudl = res_gu['MarketSegments'][indx]['MarketSegmentID']
        # print('Market Segment for the underlying {} :: {}'.format(udl, str(segmentIDudl)))

        url = 'https://a7.deutsche-boerse.com/api/v1/rdi/XETR/{}/{}?mode=detailed'.format(reference_date,
                                                                                          segmentIDudl)
        r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
        res_u = r.json()
        security = res_u['Securities'][0]

        matu_list_Stk = ['UDL']
    else:
        matu_list_Stk = []

    # Futures
    if (udl_p in index_list):
        udl_f = udl_p[4]

        lst_ms = np.array([x['MarketSegment'] for x in res_go['MarketSegments']])
        indx = np.where(lst_ms == udl_f)[0][0]
        segmentIDfut = res_go['MarketSegments'][indx]['MarketSegmentID']
        # print('Market Segment for options on {} :: {}'.format(udl, str(segmentIDopt)))

        url = 'https://a7.deutsche-boerse.com/api/v1/rdi/XEUR/{}/{}?mode=detailed'.format(
            reference_date,
            segmentIDfut)
        r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
        res_f = r.json()

        matu_list_Fut = DT_u.get_matu_list(reference_date, trim=True)[:2]
    else:
        matu_list_Fut = []

    # Options

    lst_ms = np.array([x['MarketSegment'] for x in res_go['MarketSegments']])
    indx = np.where(lst_ms == udl)[0][0]
    segmentIDopt = res_go['MarketSegments'][indx]['MarketSegmentID']
    # print('Market Segment for options on {} :: {}'.format(udl, str(segmentIDopt)))

    url = 'https://a7.deutsche-boerse.com/api/v1/rdi/XEUR/{}/{}?mode=detailed'.format(reference_date,
                                                                                      segmentIDopt)
    r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
    res_i = r.json()

    matu_list_Opt = DT_u.get_matu_list(reference_date)


def build_options_list():

    global df_orderbook

    df_u = pd.DataFrame(columns=['SegmentID'] + selected_fields + selected_fields_desc)

    i = 0
    for matu in matu_list_Stk:
        df_u.loc[i] = [segmentIDudl, security['SecurityDesc'], security['SecurityID'], 'S', None, 1, None]
        df_opt = get_quotes(df_u.loc[i])
        df_opt['matu'] = matu
        df_opt['udl'] = udl
        df_opt = df_opt.loc[(df_opt.bid > 0) & (df_opt.ask > 0)]
        df_orderbook = df_orderbook.append(df_opt)
        i += 1

    for c, matu in enumerate(matu_list_Fut):
        for x in [x for x in res_f['Securities'] if (str(x['MaturityDate']) == matu) and (x['SecurityType'] == 'FUT')]:
            df_u.loc[i] = [segmentIDfut] + [x[elt] for elt in selected_fields] + [
                x['DerivativesDescriptorGroup']['SimpleInstrumentDescriptorGroup'][elt] for elt in selected_fields_desc]
            df_u.loc[i]['PutOrCall'] = 'FUT' + str(c)
            df_opt = get_quotes(df_u.loc[i])
            df_opt['matu'] = matu
            df_opt['udl'] = udl
            df_opt = df_opt.loc[(df_opt.bid > 0) & (df_opt.ask > 0)]
            df_orderbook = df_orderbook.append(df_opt)
            i += 1

    FVUmin = (df_opt.bid.min() + df_opt.ask.min()) / 2
    FVUmax = (df_opt.bid.max() + df_opt.ask.max()) / 2

    for matu in matu_list_Opt:
        i = 0
        print('    ' + matu)

        df = pd.DataFrame(columns=['SegmentID'] + selected_fields + selected_fields_desc)

        for x in [x for x in res_i['Securities'] if
                  (str(x['MaturityDate']) == matu) and (x['SecurityType'] == 'OPT')]:
            df.loc[i] = [segmentIDopt] + [x[elt] for elt in selected_fields] + \
                        [x['DerivativesDescriptorGroup']['SimpleInstrumentDescriptorGroup'][elt] for elt
                         in selected_fields_desc]
            i += 1

        df.sort_values(by=['StrikePrice', 'PutOrCall'], ascending=[True, True], inplace=True)

        TTM = DT_u.time_between(pd.Timestamp(reference_date), pd.Timestamp(matu))
        df['matu'] = matu
        df['moneyness_T_min'] = df.apply(
            lambda opt: math.log(opt.StrikePrice / FVUmax) / (max(3.0 / 12.0, TTM) ** 0.5), axis='columns')
        # we consider that div max is 5%
        df['moneyness_T_max'] = df.apply(
            lambda opt: math.log(opt.StrikePrice / (FVUmin * 0.95)) / (max(3.0 / 12.0, TTM) ** 0.5), axis='columns')

        df['in_range'] = df.apply(lambda opt: (opt.moneyness_T_max > moneyness_range_call[0]) and (
                opt.moneyness_T_min < moneyness_range_call[1]) \
            if opt.PutOrCall == '1' else \
            (opt.moneyness_T_max > moneyness_range_put[0]) and (
                    opt.moneyness_T_min < moneyness_range_put[1]),
                                  axis='columns')

    return (df.loc[df.in_range])




a = datetime.datetime.now()  # time check

for reference_date in DT.dates_list: #[::5]:
    print(reference_date)

    # retrieve all instruments (stocks the options) from A7

    url = 'https://a7.deutsche-boerse.com/api/v1/rdi/XETR/{}?mode=detailed'.format(reference_date)
    r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
    res_gu = r.json()

    url = 'https://a7.deutsche-boerse.com/api/v1/rdi/XEUR/{}?mode=detailed'.format(reference_date)
    r = requests.get(url=url, headers={'Authorization': API_TOKEN}, proxies=proxies)
    res_go = r.json()

    for udl_p in index_list + udl_list:
        udl = udl_p[0]
        isin = udl_p[3]

        # Determine which instance of DT class : the normal one (DT)
        # or the one giving thursday expiry dor italian stocks (DTi)
        if isin[:2] == 'IT':
            DT_u = DTi
        else:
            DT_u = DT

        print('\n' + udl)

        try:
            df_orderbook = pd.read_pickle(folder1 + '/Quotes_' + udl + '.pkl')
        except:
            df_orderbook = pd.DataFrame()

        if df_orderbook.shape[0] > 0:
            done_already = [elt.strftime('%Y%m%d') for elt in set([elt.date() for elt in df_orderbook.index])]
        else:
            done_already = []

        if reference_date not in done_already:

            try:

                retrieve_instruments_from_A7()

                # retrieves quotes

                selected_fields = ['SecurityDesc', 'SecurityID']
                selected_fields_desc = ['PutOrCall', 'StrikePrice', 'ContractMultiplier', 'ExerciseStyle']

                df = build_options_list()

                for index, opt in df.iterrows():
                    # print(opt)
                    df_opt = get_quotes(opt)
                    df_opt['matu'] = opt.matu
                    df_opt['udl'] = udl
                    df_opt = df_opt.loc[(df_opt.bid > 0) & (df_opt.ask > 0)]
                    df_orderbook = df_orderbook.append(df_opt)

            except:
                print('\n\n\n fail for : {}, {}\n\n\n'.format(reference_date, udl))

            df_orderbook.to_pickle(folder1 + '/Quotes_' + udl + '.pkl')

        b = datetime.datetime.now()
        print(b - a)
        a = b
