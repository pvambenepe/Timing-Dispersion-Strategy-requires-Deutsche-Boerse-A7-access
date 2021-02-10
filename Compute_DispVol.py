from SetUp import *
# from GitImport import *
from DateAndTime import DateAndTime
from PricingAndCalibration import Pricing
from PricingAndCalibration import FittingSpline


DT = DateAndTime(from_date, until_date, force_matu=chosen_matu)
DTi = DateAndTime(from_date, until_date, force_matu=chosen_matu, ital_rule=True)

for udl_p in index_list + udl_list:
    udl = udl_p[0]
    isin = udl_p[3]
    print(udl)

    if isin[:2] == 'IT':
        FS = FittingSpline(udl, DTi, folder1, folder2)
    else:
        FS = FittingSpline(udl, DT, folder1, folder2)

    if FS.data_found:
        FS.fit_all()



def pick_hour(df_d):
    i = df_d.Error.idxmin()
    return(df.loc[i,:])

def compute_dispvol(df_d):
    W = df_d.W.sum()
    res = df_d.loc[df_d.udl == 'OESX']
    res['W'] = W * res.RefSpot / res.Spot
    res['DispVolbid'] = (df_d.DispVolbid.sum() / W - (1+Leverage) * res.ATFbid ** 2) / (2 * (1+Leverage) * res.ATFbid)
    res['DispVolask'] = (df_d.DispVolask.sum() / W - (1 + Leverage) * res.ATFask ** 2) / (2 * (1 + Leverage) * res.ATFask)
    return(res)

matu = chosen_matu[0][:-2]
# udl_dic = dict([(elt[0], (elt[1], elt[2])) for elt in udl_list])
Leverage = 0.2

df = pd.DataFrame()
for udl_p in index_list + udl_list:
    udl = udl_p[0]
    try:
        df_udl = pd.read_pickle(folder2 + '/Params_' + udl + '.pkl')
    except:
        df_udl = pd.DataFrame()

    if df_udl.shape[0] > 0:
        df_udl['udl'] = udl
        df_udl['ATFbid'] = df_udl.spline_bid.apply(lambda x: x(0))
        df_udl['ATFask'] = df_udl.spline_ask.apply(lambda x: x(0))
        s = df_udl.index.levels[1].to_series()
        df_udl.index = df_udl.index.set_levels(s.map(lambda x: x[:-2]).fillna(s), level=1)
        df_udl = df_udl.xs(matu, level=1, drop_level=True)
        df_udl = df_udl[['udl', 'ATFbid', 'ATFask', 'Spot', 'Error']]
        df_udl.index = df_udl.index.map(lambda x: x.date())
        df_udl.sort_values(by=['ts', 'Error'], inplace=True)
        df_udl = df_udl.groupby(df_udl.index).first()
        df = df.append(df_udl)


dW = pd.DataFrame(index_list + udl_list, columns=['udl', 'RefSpot', 'W', 'isin', 'info'])
df = pd.merge(df, dW, left_on='udl', right_on='udl', how='left').set_index(df.index)
df['W'] = df.apply(lambda x: 0 if x.udl == 'OESX' else x.W / 100 * (x.Spot / x.RefSpot), axis='columns')
df['DispVolbid'] = df.apply(lambda x: x.W * x.ATFbid ** 2, axis='columns')
df['DispVolask'] = df.apply(lambda x: x.W * x.ATFask ** 2, axis='columns')
df = df.groupby(df.index, group_keys=False).apply(compute_dispvol)
print(df)

df = df.loc[df.W > 0.8*df.W.max()]

x = df['ATFbid'].values
y = df['DispVolbid'].values
dates = [elt.strftime('%m/%d') for elt in df.index.values]

u = np.diff(x)
v = np.diff(y)
pos_x = x[:-1] + u/2
pos_y = y[:-1] + v/2
norm = np.sqrt(u**2+v**2)

fig, ax = plt.subplots()
ax.plot(x,y, marker="o")
ax.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid")

for i, txt in enumerate(dates):
    if i%4==0:
        # ax.annotate(txt, (x[i], y[i]))
        ax.annotate(txt, (x[i], y[i]), xytext=(10, 10), textcoords='offset points')

plt.scatter([x[-1]], [y[-1]], c='#ff0000', s=120)

plt.xlabel("index implicit vol")
plt.ylabel("dispersion vol")
plt.show()

print('end')

