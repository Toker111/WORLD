import pandas as pd
import matplotlib.pyplot as plt

def clear_excel():
    df_empty=pd.DataFrame()
    with pd.ExcelWriter('output.xlsx',mode='a',engine='openpyxl',if_sheet_exists='replace') as writer:
        df_empty.to_excel(writer, sheet_name='Sheet1', index=False)


clear_excel()





df = pd.read_excel('output.xlsx')
#subplots会返回一个nrows * ncols 的二维数组
fig,axes= plt.subplots(2,2,figsize=(12,5))
ax1, ax2, ax3, ax4 = axes.flatten()
ax1.scatter(df['vision_range'],df['age'],s=10, alpha=0.5)
ax1.set_title('Vision Range')
ax1.set_xlabel('Vision Range')
ax1.set_ylabel('Age')

ax2.scatter(df['move_cost'],df['age'],s=10, alpha=0.5)
ax2.set_title('Move Cost')
ax2.set_xlabel('Move Cost')
ax2.set_ylabel('Age')

ax3.scatter(df['vision_range'],df['move_cost'],s=10, alpha=0.5)
ax3.set_xlabel('Vision Range')
ax3.set_ylabel('ove_cost')



fig.tight_layout()
plt.show()