from matplotlib.mlab import griddata
import matplotlib.pyplot as plt

class Plot:

    def plot(self, net, examples, labels):
        xes = []
        yes = []
        res = []
        y = -1
        while y<=1:
            x = -1
            while x<=1:
                result = net.predict([[x], [y]])
                xes.append(x)
                yes.append(y)
                res.append(result[0][0])
                x+=0.05
            y+=0.05

        zi = griddata(xes, yes, res, xes, yes, interp='linear')

        plt.contourf(xes, yes, zi, 15, vmax=abs(zi).max(), vmin=-abs(zi).max())

        plt.scatter(examples[0], examples[1], 3, color=['red' if v else 'blue' for v in labels[0]])
        plt.show()

