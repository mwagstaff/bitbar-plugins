#!/usr/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Tube Status</bitbar.title>
# <bitbar.version>v1.0.0</bitbar.version>
# <bitbar.author>Mike Wagstaff</bitbar.author>
# <bitbar.author.github>mwagstaff</bitbar.author.github>
# <bitbar.desc>Realtime TFL status for tube, Overground, DLR and TFL Rail</bitbar.desc>
# <bitbar.image>https://cloud.githubusercontent.com/assets/2979988/17312884/82658b1c-584e-11e6-9309-a006bc3aee03.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/mwagstaff/bitbar-tube-status/</bitbar.abouturl>

# Required libraries
import urllib2
import json
import sys

# Use UTF-8 encoding to enable emoji support
reload(sys)  
sys.setdefaultencoding('utf8')

# An array of your favourite lines, i.e. those that you want to be notified of in the menu bar
# Leave the array blank to be notified for all lines
# Note that all lines will still have their status displayed in the dropdown, regardless of its contents
linesFavourite = [ "Bakerloo", "DLR", "Central", "District", "Jubilee", "Northern", "Piccadilly" ]

# The colour to use for "bad" line status updates in the menu bar
colorBadLineText = "black"

# The prefix to display for good / bad line statuses
prefixLineStatusGood = "✅"
prefixLineStatusBad = "⚠️"

# The TFL Tube Status API URL that will be called to get the data
apiTflStatusUrl = "https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status"

# Base64 encoded TfL logo
logo_image = "iVBORw0KGgoAAAANSUhEUgAAAC4AAAAiCAYAAAAge+tMAAAMFWlDQ1BJQ0MgUHJvZmlsZQAASImVVwdYU8kWnltSCAktEAEpoTdBepXeO9LBRkgChBIgIajYy6KCa0FFBERFV0AUXQsga8WuLAL2+kBFZWVdLNhQeZMCur72vfN9c+/PmXPO/Ofk3GEGAEVrVl5eNqoEQA6/QBAd6MNMTEpmknoBGSCAAmwAymIL87yjosIAlLH33+XdTWgL5ZqlONa/zv9XUeZwhWwAkCiIUzlCdg7EhwHA1dl5ggIACB1QbzC7IE+MhyBWFUCCABBxMU6XYnUxTpXiSRKb2GhfiL0AIFNZLEE6AApi3sxCdjqMoyDmaM3n8PgQV0Pswc5gcSC+D/GknJxciBXJEJumfhcn/W8xU8djsljp41iai0TIfjxhXjZr7v9Zjv8tOdmisTX04aBmCIKixTnDutVn5YaKMRXiY/zUiEiIVSC+yONI7MX4boYoKE5mP8gW+sKaAQYAKOCw/EIh1oKYIcqK85ZhW5ZA4gvt0QheQXCsDKcKcqNl8dFCfnZEmCzOygxu8Biu4Qr9Y8Zs0ngBwRDDTkMPF2XEJkh5omcLefERECtA3CXMigmV+T4syvCNGLMRiKLFnA0hfpsmCIiW2mDqOcKxvDArNkuyFuwFzKsgIzZI6oslcoWJYWMcOFw/fykHjMPlx8m4YbC7fKJlvsV52VEye6yGmx0YLa0zdkBYGDPm21MAG0xaB+xRJiskSrbWu7yCqFgpNxwFYcAX+AEmEMGRCnJBJuB1DrYMwr+kMwGABQQgHXCBpUwz5pEgmeHDZwwoAn9CxAXCcT8fySwXFEL9l3Gt9GkJ0iSzhRKPLPAU4hxcE/fA3fAw+PSCwxZ3xl3G/JiKY6sS/Yl+xCBiANFsnAcbss6GQwB4/0YXCt9cmJ2YC38sh2/xCE8J3YRHhBuEXsIdEA+eSKLIrGbxlgp+YM4E4aAXRguQZZcKYw6M2eDGkLUD7oO7Q/6QO87ANYElbg8z8cY9YW4OUPs9Q9E4t2+1/HE9Mevv85HpFcwVHGQsUsd/Gd9xqx+j+H5XIw58h/5oia3EDmEXsNPYJewY1gKY2EmsFevAjovxeCc8kXTC2GrREm5ZMA5vzMa60XrA+vMPa7Nk64vrJSzgzikQfwy+uXlzBbz0jAKmN9yNucxgPttqEtPW2sYRAPHeLt063jAkezbCuPxNl38KAJcSqEz/pmMZAHD0KQD0d990Bq9hu68D4HgXWyQolOrE2zEgwP8YivCr0AA6wACYwnxsgSNwA17AH4SASBALksBMWPEMkAM5zwbzwRJQDErBOrAJVIJtYCeoB/vAQdACjoHT4Dy4ArrADXAP9kU/eAGGwDswgiAICaEhdEQD0UWMEAvEFnFGPBB/JAyJRpKQFCQd4SMiZD6yDClFypBKZAfSgPyKHEVOI5eQbuQO0ocMIK+RTyiGUlFVVBs1Riejzqg3GorGojPQdDQfLUKXo2vQCrQW3Ys2o6fRK+gNtBd9gQ5jAJPHGJgeZok5Y75YJJaMpWECbCFWgpVjtVgT1gZ/52tYLzaIfcSJOB1n4pawN4PwOJyN5+ML8dV4JV6PN+Nn8Wt4Hz6EfyXQCFoEC4IrIZiQSEgnzCYUE8oJuwlHCOfgd9NPeEckEhlEE6IT/C6TiJnEecTVxK3E/cRTxG7iY+IwiUTSIFmQ3EmRJBapgFRM2kLaSzpJ6iH1kz6Q5cm6ZFtyADmZzCcvJZeT95BPkHvIz8gjckpyRnKucpFyHLm5cmvldsm1yV2V65cboShTTCjulFhKJmUJpYLSRDlHuU95Iy8vry/vIj9Vnie/WL5C/oD8Rfk++Y9UFao51Zc6nSqirqHWUU9R71Df0Gg0Y5oXLZlWQFtDa6CdoT2kfVCgK1gpBCtwFBYpVCk0K/QovFSUUzRS9FacqVikWK54SPGq4qCSnJKxkq8SS2mhUpXSUaVbSsPKdGUb5UjlHOXVynuULyk/VyGpGKv4q3BUlqvsVDmj8piO0Q3ovnQ2fRl9F/0cvV+VqGqiGqyaqVqquk+1U3VITUXNXi1ebY5aldpxtV4GxjBmBDOyGWsZBxk3GZ8maE/wnsCdsGpC04SeCe/VJ6p7qXPVS9T3q99Q/6TB1PDXyNJYr9Gi8UAT1zTXnKo5W7NG85zm4ETViW4T2RNLJh6ceFcL1TLXitaap7VTq0NrWFtHO1A7T3uL9hntQR2GjpdOps5GnRM6A7p0XQ9dnu5G3ZO6fzDVmN7MbGYF8yxzSE9LL0hPpLdDr1NvRN9EP05/qf5+/QcGFANngzSDjQbtBkOGuobhhvMNGw3vGskZORtlGG02umD03tjEOMF4hXGL8XMTdZNgkyKTRpP7pjRTT9N801rT62ZEM2ezLLOtZl3mqLmDeYZ5lflVC9TC0YJnsdWiexJhkssk/qTaSbcsqZbeloWWjZZ9VgyrMKulVi1WLycbTk6evH7yhclfrR2ss613Wd+zUbEJsVlq02bz2tbclm1bZXvdjmYXYLfIrtXulb2FPde+xv62A90h3GGFQ7vDF0cnR4Fjk+OAk6FTilO10y1nVeco59XOF10ILj4ui1yOuXx0dXQtcD3o+pebpVuW2x6351NMpnCn7Jry2F3fneW+w73Xg+mR4rHdo9dTz5PlWev5yMvAi+O12+uZt5l3pvde75c+1j4CnyM+731dfRf4nvLD/AL9Svw6/VX84/wr/R8G6AekBzQGDAU6BM4LPBVECAoNWh90K1g7mB3cEDwU4hSyIORsKDU0JrQy9FGYeZggrC0cDQ8J3xB+P8Iogh/REgkigyM3RD6IMonKj/ptKnFq1NSqqU+jbaLnR1+IocfMitkT8y7WJ3Zt7L040zhRXHu8Yvz0+Ib49wl+CWUJvYmTExckXknSTOIltSaTkuOTdycPT/Oftmla/3SH6cXTb84wmTFnxqWZmjOzZx6fpTiLNetQCiElIWVPymdWJKuWNZwanFqdOsT2ZW9mv+B4cTZyBrju3DLuszT3tLK05+nu6RvSBzI8M8ozBnm+vEreq8ygzG2Z77Mis+qyRrMTsvfnkHNSco7yVfhZ/LO5OrlzcrvzLPKK83rzXfM35Q8JQgW7hYhwhrC1QBUeczpEpqKfRH2FHoVVhR9mx88+NEd5Dn9Ox1zzuavmPisKKPplHj6PPa99vt78JfP7Fngv2LEQWZi6sH2RwaLli/oXBy6uX0JZkrXk96XWS8uWvl2WsKxtufbyxcsf/xT4U2OxQrGg+NYKtxXbVuIreSs7V9mt2rLqawmn5HKpdWl56efV7NWXf7b5ueLn0TVpazrXOq6tWUdcx193c73n+voy5bKisscbwjc0b2RuLNn4dtOsTZfK7cu3baZsFm3urQiraN1iuGXdls+VGZU3qnyq9ldrVa+qfr+Vs7WnxqumaZv2ttJtn7bztt/eEbijuda4tnwncWfhzqe74ndd+MX5l4bdmrtLd3+p49f11kfXn21wamjYo7VnbSPaKGoc2Dt9b9c+v32tTZZNO/Yz9pceAAdEB/74NeXXmwdDD7Yfcj7UdNjocPUR+pGSZqR5bvNQS0ZLb2tSa/fRkKPtbW5tR36z+q3umN6xquNqx9eeoJxYfmL0ZNHJ4VN5pwZPp59+3D6r/d6ZxDPXz04923ku9NzF8wHnz1zwvnDyovvFY5dcLx297Hy55YrjleYOh44jvzv8fqTTsbP5qtPV1i6XrrbuKd0nejx7Tl/zu3b+evD1KzcibnTfjLt5+9b0W723Obef38m+8+pu4d2Re4vvE+6XPFB6UP5Q62HtP8z+sb/Xsfd4n19fx6OYR/cesx+/eCJ88rl/+VPa0/Jnus8ants+PzYQMND1x7Q/+l/kvRgZLP5T+c/ql6YvD//l9VfHUOJQ/yvBq9HXq99ovKl7a/+2fThq+OG7nHcj70s+aHyo/+j88cKnhE/PRmZ/Jn2u+GL2pe1r6Nf7ozmjo3ksAUtyFMDgQNPSAHhdBwAtCZ4dugCgKEjvXhJBpPdFCQL/CUvvZxKBJ5c6LwDiFgMQBs8oNXAYQUyFb/HRO9YLoHZ240MmwjQ7W2ksKrzBED6Mjr7RBoDUBsAXwejoyNbR0S+7INk7AJzKl975xEKE5/vtVmLU1f8S/Cj/BEMkbPL7q6VCAAAACXBIWXMAABYlAAAWJQFJUiTwAAACBmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8ZXhpZjpQaXhlbFlEaW1lbnNpb24+MTY1MDwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4yMjE4PC9leGlmOlBpeGVsWERpbWVuc2lvbj4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CswpkuAAAAnfSURBVFgJrVgLcFTlFf72/cqGQHgmkCKE8AiEMJjIS0QZFaGlhSIjKrUUOi10OrV2prXVobY6pdqp2E6ndKTD2FKpIsNDCeJQQIfSUCAYApFHSCAkAUJeZLPP7CM9339zdxbdhU3smdl7797//Od8//nP67+GHiH0k2IxTu2B0WhMKYHi+TMYDOqXkrGPA4b+ACdgwXEbkHA4imCoG7FYDAIRZosJDrv1Np5k8/qIN85ujj+l8aBvjtEoqIWuN3fgs/NNqPqsCRdq29HQ7Ic/FIVJxge6LcjPG4DCgiEoKhyFcWNHwOGwqnlc3J12STHd5ZK2xROV1V1pxvv7T+ONHRdRf9ALmMVVxooNMuRu0haFUAxoiwKNEWCwCU8+PgwrlxZh7uyJcDpsyn2IjS7UH0oLuA7aHwhh+67jWPXCceBKBCMecGKoyyQggKj89B1RQASPUUBxHRFxrepr3UBVAEtX52D9s/MwdfJoxab7f1/B3xW4Dvpmayde+E0Z/rqxHgUPu5FhM6EjEBVvBlxWo4AEwoI+IoamEa2CmO+65Z0v3AOXxaD4Tl4OAOcj2LX7QXxjUUm/wd8RuA666Xo7nvrRDnxyqBOls91o9UUQEkDZThMC4RhqzgU1l7CagJHiLiExf5O4CWm6DcXDrfB398ArvNkOE2KyRdX7O/DWtgfwzIr7FVtfLZ8SODMAg9DTFcAzz76D3QfaUDLNhSZPBHaxZoZYueq/PsBtxPOr78GM6XkYmTMILqcNkWgUHbd8OF/TjN3/qsW+rTdhnOlEYZYFbbJLtL5bFnmqrB17yhZg8cLp8ZSpVpHGJSnwxNX/9o19+PmPq1C6OAtXO8OiUNxCBF844MVLr07EU8tKMfaeYSmDzOsLovz4Rfzs9aP49IIfxeMcaPFH4TAbYJNf9X4vzlSvwORJeSqVppttkgLXXaT8xEXMKt2JaYsy0SrKbGJp1py6igB2bp2HJV/VfJQG0otRorESi86N5ltY/9o+bN7ShOLZLjT7ohgirlZVE8C3HxuOv7y2HDabJW3L03i3Ea3NVYdCYWz6u2SPQqsEnZa2HBYj6g76sX/HI3HQUcnJ2hwJRpmX+CNwjkWjMQwfloXf/2oJvvudXFTWBjFYfL1d3GZagQNv/bEBR8rPKxzMUOlQHDgVMGhobdLZcw3Y+qdGFOXZ4ZGcPMhhxJkPPdi4qRiPzp8aB8SUR1JzZX5cTq884mCshCNRuDMcWP/cozBmm1ErseKQ/E+jYIIV7+09i+7uiOIlBu4gZaWiOHBaR+Vdk2QGoSPHLsmVVoT4IlDZEsbDKwZj1ZNz1Dj5TSaj8m19LucnPvO//s5i1uSOzM3G3l/Ohf+oX9KjBL8YZdJXbHjz7SbUN7Qo2dquabJSQVclnyvz+ULgtptFgcfjx6FjjUCJDT5JY05xERz34Ztri2CzWtAp4wTYV6Ieq8WMCQU5mLIwEw1i9QES7FYJUtyI4FRVPfJGDUEwKMVKiL2O1aogfkGVCk4yPv/KHhw904acQVbc8kZQ1xaCWcCprRa5/kgPJg2zwy6KVCD2AziXSpcyS5A3tobQIj7OgKeSsLhGlt2EUdk2pWP3+S6U/2EBZpQUKPflLiSSZnF5c6PFj5Mfd8EowUg3H52hlXIys5y7xCqHG/xacbldRqK89J5Ffk6mSYGmG9M4rLStspDqc11qDOWdYMeZihRwWsLlkMd8C4oGWZR7sFTrxHExOMZKX2Jxa7ugj/X1TlmUHBKBBE3iO6rLkMI0INuCLMk412BVgaoYklziDqSEyGRlAV1ikgnM41+G7jRd6ZZV3IlH1x13lRC3pTWCZtlCP/sQm/hyggS64vVATI1ZJb1FRTwtpdmLdzLzjT7p888aDw8Z9OccuwSlCNVtRO+TVgZ10geNUy8jKh44KxnFXSUzw4rcfDsKhtjQLpNvyo+BQxmEwKaqeKhNsolsqyjoR2wq/QxOu2SpNkkALEA0ApdKI0l2xYzhdmTIomrGOOR/6mBSWYVZwtPlVxWO+Zbpbu0v9qDsQhfyMy0q357e14VNW0rw9PJZqqp+mXTIFnnZD3eh3hPGQMlSmbK7lSL/7e334+uLpsfTIRs2u6REZTxaL4GUxVnZsga44q8zM5146L5clG09jYxFVhWsuNeGvYcvK+DZg9xx3v48HDtZg8qyThRLD9Tuj6mDBjKNuHfaaNVdErBO3I1kuxvfCxYH/thXkObMyJcr2wAtAxQPtcpCWvCPd/+jxlmWyavPu9udJZ/Ec+q6DUeAmQ7Vo7ttBpxtDGHVqhxVfMijSn4vns8ZmsOK4sC59apci/VJRYV5eOL7Oai6GgSFdwRjKFzgxtrVJ3Dok7OSqoyq5NNn9bnJ7pRFV6QL+v0hvPL6R7h0KYgi6c39clxigOJsCE8sngK7dIfkVSW/Fw/nJ6M4cH2Qyrli+ta6ldK2ilC7NENRAcjcPvohF+av+QgfHqhUU/QA0hojrTmicu2/tij2NG3tXXhxw/v48+YGFE9yqGIzUCrlp1eCYqBczJk5XslL5hY6tsT7F4BzkOBJc2ZOxK9/NxkVez0Y4TajS/oWWmiMNEULH9mPDRvLcOXqTcWrNUZsa9mY8ac9B6Sd+Pjf1fjamm3YuKUeU2e60CK9OA8Siqql3fjBXHXy52J13dpg6mvSgwTZtS0zoL3Di+Xr/omDFR6UTHCisSsCpyh1SUqrksYLoy14eUU+SqflIXdElnw7sSnfv9XpQ01tM8oO12LbpuuS5+yYKlVZP/0MlOp48oN2vLtzPpYvmaFihYk3XYunBK6B1z7cXG1sxdJ1O1Bx2ovSYjm9eKMqaAdKvr0VjOLqcTm5ixVhlNaV31eCEtENYREh9yl2TBlpU27m6Za+Xubwg1HVvnZs/tscrPnWPKpSwNO1NvnvCJwM3D5uO0/6z730Aba/eU2CNFO+ARngFSDMOjw4W+R/SIKNhYo9uEP6Dt79Ug7Zl9i5S5KvK5pCwKkgtr03FyuWzaKK+O6qP2le7gpcE6yB58F3245yfO+nFYA3hlH3OTDYaVaBS3BcRK/nKvX8wGWTCz8InbkpPbacVR97eihe/smDmF48RvHoLpkm3jhbWsDJrVuez+cuNmLn3kq8+E4tcEJaXX5PGW+BQT7BZYul2XN08hNcq7jPZbqMAQtXDsaax4swf14hMt3OXp+WkXSdmooTKG3gnKNyttx1ZY1NbXI2bcTp6iack4+eddf9aJHgpVvkyoGgIM+NyeOHonjyKBSMy0GGy65Ua9mDxz71t1+XPgGnBvEG9PT6faJGpr1AoFuaf+3Aa7NZJcVZ1VFQ56NbEKy+cP19f+59Bq4rkXoU327m7VSktQIE+/8BrOv5H+BBuytlXzclAAAAAElFTkSuQmCC"

def main():

  # Get the TFL feed data from the API
  tflData = getTflApiData(apiTflStatusUrl)

  # Get all the line names (to display the status summary for each line in the dropdown)
  linesAll = getLinesAll(tflData)

  # Get the status data for each line
  lineStatusData = getLineStatusData(tflData)

  # Get a summary of "bad" lines, and print it in the menu bar
  linesSummaryBad = getLineStatusSummaryBad(lineStatusData, linesFavourite, linesAll)
  printLineStatusSummary(linesSummaryBad)

  # Print the summary of "good" lines
  printLineStatusAll(lineStatusData, linesAll, linesFavourite)


# Get the line status data from the TFL feed API
def getTflApiData(apiTflStatusUrl):
  response = urllib2.urlopen(apiTflStatusUrl)
  tflData = json.load(response)

  return tflData


# Get a list of all tube lines
def getLinesAll(tflData):

  linesAll = []

  for tubeLine in tflData:

    if tubeLine["name"] not in linesAll:
      linesAll.append( tubeLine["name"] )

  return linesAll


# Get the status data for all lines
def getLineStatusData(tflData):

  lineStatusData = []

  for tubeLine in tflData:

    # If one or more line statuses has been posted...
    if len( tubeLine["lineStatuses"] ) > 0:

      # For each line status, flag it up if it's anything other than good service
      for lineStatus in tubeLine["lineStatuses"]:

        reason = None
        if "reason" in lineStatus.iterkeys():
          reason = lineStatus["reason"]

        lineStatusData.append({
          "name" : tubeLine["name"],
          "statusSeverity" : lineStatus["statusSeverity"],
          "statusSeverityDescription" : lineStatus["statusSeverityDescription"],
          "reason" : reason
        })

  return lineStatusData


# Get the line status for the given line
def getLineStatus(lineStatusData, name):

  lineStatus = {
    "statusSeverity" : 10,
    "statusSeverityDescription" : "Good Service",
    "reason" : ""
  }

  for line in lineStatusData:
    if line["name"] == name:
      if line["statusSeverity"] < lineStatus["statusSeverity"]:
        lineStatus["statusSeverity"] = line["statusSeverity"]
        lineStatus["statusSeverityDescription"] = line["statusSeverityDescription"]
        if "reason" in line.iterkeys():
          lineStatus["reason"] = line["reason"]

  return lineStatus


# Get a summary text of "bad" lines that we're interested in
def getLineStatusSummaryBad(lineStatusData, linesFavourite, linesAll):

  linesSummaryBad = ""
  linesStatusBad = 0

  if len(linesFavourite) == 0:
    linesFavourite = linesAll

  for line in linesFavourite:

    lineStatus = getLineStatus(lineStatusData, line)

    if lineStatus["statusSeverity"] < 10:
      linesStatusBad += 1

      if linesStatusBad > 1:
        linesSummaryBad += ", "

      linesSummaryBad += line + ": " + lineStatus["statusSeverityDescription"]

  return linesSummaryBad


# If by some miracle, everything is good, then relay the joyous news in the menu bar
# Otherwise, print out the summary of the damage for the lines we're interested in
def printLineStatusSummary(linesSummaryBad):

  lineStatusSummary = ""

  if len(linesSummaryBad) == 0:
    lineStatusSummary += "Good service | color=gray"
  else:
    lineStatusSummary += linesSummaryBad + " | color=" + colorBadLineText

  print lineStatusSummary + " image=" + logo_image

  print "---"


def getLineStatusUri(line):
  uriPrefix = "https://tfl.gov.uk/tube-dlr-overground/status/#"

  if "DLR" in line:
      return uriPrefix + "line-dlr-dlr"
  elif "London Overground" in line:
    return uriPrefix + "line-raillo-overground"
  elif "TfL Rail" in line:
    return uriPrefix + "line-tfl-rail"
  else:
    return uriPrefix + "line-lul-" + line.lower().replace(" & ", "-")


# Print the status for all lines in the dropdown
def printLineStatusAll(lineStatusData, linesAll, linesFavourite):

  linesSummaryAll = ""
  linesStatusAll = 0

  for line in linesAll:

    lineStatus = getLineStatus(lineStatusData, line)
    
    linesSummaryAll += prefixLineStatusBad if lineStatus["statusSeverity"] < 10 else prefixLineStatusGood

    # Highlight lines of interest
    if line in linesFavourite:
      linesSummaryAll += " *"
    else:
      linesSummaryAll += " "

    linesSummaryAll += line + ": "

    if lineStatus["reason"]:
      linesSummaryAll += lineStatus["reason"]
    else:
      linesSummaryAll += lineStatus["statusSeverityDescription"]

    linesSummaryAll += " | href=" + getLineStatusUri(line) + " \n"

  print linesSummaryAll


main()