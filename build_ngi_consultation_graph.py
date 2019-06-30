# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp
import csv

def build_posts_list():
  '''
  (none) => list of dicts
  consultation.ngi.eu is a blogging platform, made up of posts and comments. 
  I want to compare it with edgeryders.ngi.eu, which is a forum platform made up of topics and posts.
  I need to build a list of dictionaries, where each item is a post or a comment. Each of them is attributed to its 
  author via the username field. Comments are assumed to be reply to posts, so to the author of the post.
  '''
  
  dirPath = '/Users/albertocottica/Documents/GitHub/scraping_ngi_consultation_network/'
  postfile = dirPath + 'posts_data.csv'
  commentsfile = dirPath + 'comments_data.csv'
  
  theList = [] # the accumulator
  with open (postfile, 'r') as pfile:
    reader = csv.DictReader(pfile)
    for row in reader:
      theList.append(row)
  with open (commentsfile, 'r') as cfile:
    reader2 = csv.DictReader(cfile)
    for row in reader2:
      theList.append(row)
  print 'There are ' + str(len(theList)) + ' posts + comments'
  return theList
      
  
def count_words(postList):
  '''
  (list of dicts) => int
  counts the words in the posts contained in postList
  '''
  words = 0
  for item in postList:
    words += len(item['text'].split())
  return words

def main(graph): 
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
  viewLabel = graph.getStringProperty("viewLabel")
  viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = graph.getColorProperty("viewLabelColor")
  viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewMetric = graph.getDoubleProperty("viewMetric")
  viewRotation = graph.getDoubleProperty("viewRotation")
  viewSelection = graph.getBooleanProperty("viewSelection")
  viewShape = graph.getIntegerProperty("viewShape")
  viewSize = graph.getSizeProperty("viewSize")
  viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
  viewTexture = graph.getStringProperty("viewTexture")
  viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
  username = graph.getStringProperty('username')
  channel = graph.getStringProperty('channel')
  
  def addnodes(postList):
    '''
    (list) => None
    induce nodes from the 'username' field in each item. Also add the 'channel' property. There are 14 channels.
    '''
    unique_users = []
    for item in postList:
      user = item['username']
      if user not in unique_users:
        unique_users.append(user)
        n = graph.addNode()
        username[n] = user
        channel[n] = item['channel']
      
  def addedges(postList):
    '''
    (list) => None
    induce edges from the 'username' fields in each item, and the 'post' field in the comment items.
    Also add the 'channel' property.
    '''

    # induce edges. To do that, I need a map going from posts to their authors, so...
    
    post2author = {}
    for item in postList:
      if 'post' not in item: # means that item encodes a post, not a comment
        post2author[item['title']] = item['username'] # using the title as unique identifier
    print (len (post2author))
      
    # induce edges discarding self-loops
    
    for item in postList:
      author = item['username']
      if 'post' in item: # if this is true, the item encodes a comment, which encodes an edge
        postAuthor = post2author[item['post']]
        for n in graph.getNodes():
          if username[n] == author:
            source = n
        for n2 in graph.getNodes():
          if username[n2] == postAuthor:
            target = n2
        e = graph.addEdge(source, target)
        channel[e] = item['channel']
          
    
  posts = build_posts_list()
#  success = addnodes(posts)
#  success = addedges(posts)
  nw = count_words(posts)
  print (nw)
