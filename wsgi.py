from app import app, Delete
from CBI import cbidict as thing

if __name__ == "__main__":
  #Delete()
  #DELETES ENTIRE DATABASE
  debug = thing["debug"][0] if thing is not None else False
  app.run(debug=debug) #<- This might not work. If it doesn't, use app.run(debug=True) or smth...

#I'm so skibidi I'm so skibidi skibidi skibidi skibidi biden. I'm so skibidi I'm so skibidi skibidi skibidi skibidi biden
#If you're reading this, you've committed a felony, I think.
#
#Hello, world! I'm the most garbage programmer ever, but I'm the best Glorbenia's got lwk
#-Diggy Gorgonzola, Oct 7th 2025
#
# Wow this was a long time ago... It's November 17th 2025 now.
