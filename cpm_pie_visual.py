import plotly
import plotly.graph_objs as go
import ec2_reader as er
import boto3


b3c = boto3.client('ec2')
response = b3c.describe_instances().get("Reservations")

def ec2visual():
  x = er.get_team_cpm(response)
  team = x.keys()
  values = x.values()

  y = er.get_product_cpm(response)
  product = y.keys()
  values2 = y.values()

  fig = {
    "data": [
      {
        "values": values,
        "labels": team,
        "domain": {"x": [0, .48]},
        "name": "Cost Per Team/ Month",
        "hoverinfo":"label+value+name",
        "textinfo": "percent",
        "hole": .4,
        "type": "pie"
      },
      {
        "values": values2,
        "labels": product,
        "text":"product",
        # "textposition":"outside",
        "domain": {"x": [.52, 1]},
        "name": "Cost Per Product/ Month",
        "hoverinfo":"label+value+name",
        "textinfo": "percent",
        "hole": .4,
        "type": "pie"
      }],
    "layout": {
          "title":"Team vs. Product Cost Per Month. Total Allocation: $%s" %("{:,}".format(er.get_total_team_cpm(response))),
          "annotations": [
              {
                  "font": {
                      "size": 20
                  },
                  "showarrow": False,
                  "text": "Team",
                  "x": 0.22,
                  "y": 0.5
              },
              {
                  "font": {
                      "size": 20
                  },
                  "showarrow": False,
                  "text": "Product",
                  "x": 0.79,
                  "y": 0.5
              }
          ]
      }
  }
  plotly.offline.plot(fig, filename='cpm_donut_representation')

