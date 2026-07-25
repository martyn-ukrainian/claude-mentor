import numpy as np
from sklearn.metrics import r2_score

y_true = [3, 5, 2, 8, 4]
y_pred = [3, 5, 2, 8, 4]

r2 = r2_score(y_true, y_pred)
print(f"A r2: {r2}")


# B
y_pred_B = [3.1, 4.9, 2.2, 7.8, 4.1]

print(f"B mean: {np.array(y_pred_B).mean()}")


r2_B = r2_score(y_true, y_pred_B)
print(f"B r2: {r2_B}")


y_pred = [4.4, 4.4, 4.4, 4.4, 4.4]
r2 = r2_score(y_true, y_pred)
print(f"C r2: {r2}")

y_pred = [10, 10, 10, 10, 10]
r2 = r2_score(y_true, y_pred)
print(f"D r2: {r2}")


y_pred = np.array([3, 5, 2, 8, 4])
y_pred_C = np.array([4.4, 4.4, 4.4, 4.4, 4.4])


print(y_pred.mean())
ss_res = np.sum((y_true - y_pred_C) ** 2)
ss_tot = np.sum((y_true - np.array(y_true).mean()) ** 2)

print(f"C ss_res: {ss_res}, ss_tot: {ss_tot}")


y_pred_E = np.array([5, 5, 5, 5, 5])


print(y_pred_E.mean())
ss_res_E = np.sum((y_true - y_pred_E) ** 2)
ss_tot_E = np.sum((y_true - np.array(y_true).mean()) ** 2)

print(f"E ss_res: {ss_res_E}, ss_tot: {ss_tot_E}")
print(r2_score(y_true, y_pred_E))
