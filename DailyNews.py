from tkinter import *
import tkinter.ttk as ttk
import praw
import webbrowser
import time


def callback(link):
	"""When a button is clicked, the link attached to that button is opened in a new tab"""
	webbrowser.open_new(link)


def refresh_fn(tab):
	"""When the refresh button is clicked, the tab in which the refresh button was in is destroyed and a new tab is 
created (takes about 1-3 seconds) """
	tab.destroy()
	main(tab)

	
def refresh_button(tab):
	""" Create a button that refreshes the tab so the most recent links are available.
The button is avaliable in each tab and on command only refreshes the current tab"""
	refresh = Button(tab, text='RF', height=1, width=2)
	refresh.grid(row=6, column=1)
	refresh.bind("<Button-1>", lambda event, tab_to_use = tab : refresh_fn(tab_to_use))

	
def buttons(tab, title, domain, hyperlink, row_num, col_num):
	link = Button(tab, text=title + ' ('+ domain + ')' , 
			height=6, width=25, justify = 'center',
			wraplength=150, fg="black", cursor="hand2")
	link.grid(row=row_num, column=col_num)
	link.bind("<Button-1>", lambda event, link = hyperlink : callback(link))
	
def buttons_no_grid(tab, title, domain, hyperlink):
	link = Button(tab, text=title + ' ('+ domain + ')' , 
			height=6, width=25, justify = 'center',
			wraplength=150, fg="black", cursor="hand2")
	link.pack()
	link.bind("<Button-1>", lambda event, link = hyperlink : callback(link))

	
def get_latest_PDS(tab):
	"""Gets links to latest PDS/Vlogs/DeFrancoFam videos thanks to posts by reddit bot "Trey-Mazing
on /r/DeFranco"""
	row=0
	col=0
	reddit = praw.Reddit(client_id='',
		client_secret='',
		user_agent='Link and title extraction')
	PDS_bot = reddit.redditor('Trey-Mazing')
	PDS_post = PDS_bot.submissions.new(limit=10)
	for post in PDS_post:
		if post.link_flair_text != None:
			buttons(tab, str(post.link_flair_text) + ' - '+post.title, 'youtube.com', post.url, row, col)
		else:
			buttons(tab, post.title, 'youtube.com', post.url, row, col)
		if col==1:
			row+=1
			col=0
		else:
			col+=1
		if row==2:
			break
	refresh_button(tab)

	
def get_rs_news(tab):
	"""Searches /r/runescape for keywords at the start of the post title for in-game news
and retrieves the links to those posts"""
	col=0
	title_content = ['TL;DR','TL;DW','Patch Notes', 'Dev Blog']
	reddit = praw.Reddit(client_id='',
					client_secret='',
					user_agent='Link and title extraction')
	subreddit = reddit.subreddit('runescape')
	submissions = subreddit.hot(limit=25)
	for submission in submissions:
		if any(keyword in submission.title for keyword in title_content):
			buttons(tab, submission.title, submission.domain, submission.url, 5, col)
			col+=1
		if col == 2:
			break


def get_reddit_links(tab, sub, number=3, Tag=''):
	"""Recieves sub name and post numbers as a module and gets that many links from the sub requested.
Also allows for iltering by tag"""
	i=0
	row=0
	col=0
	reddit = praw.Reddit(client_id='',
		client_secret='',
		user_agent='Link and title extraction')
	subreddit = reddit.subreddit(sub)
	submissions = subreddit.hot()
	if Tag != '':
		for submission in submissions:
			if submission.link_flair_text == Tag:
				buttons(tab, submission.title, submission.domain, submission.url, row, col)		
				i+=1
				if i == number:
					break
				if col == 1:
					row+=1
					col=0
				else:
					col+=1
	else:
		for submission in submissions:
			if not submission.domain.startswith('self.'): #Makes sure only news links are posted
				buttons(tab, submission.title, submission.domain, submission.url, row, col)
				i+=1
				if i == number:
					break
				if col == 1:
					row+=1
					col=0
				else:
					col+=1
	i=0
	row=0
	col=0
	refresh_button(tab)

def main(tab):
	"""Main loop that initializes the Tkinter frame"""
	global root
	global tab1,tab2,tab3,tab4,tab5
	global nb
	start_time = time.time()
	
	if tab == '':
		root = Tk()
		root.title('Personalized News')
		root.geometry('375x480')
		root.configure
		nb = ttk.Notebook(root)
	#If-statements below allow for only specific tabs to be refreshed if the refresh button is clicked
	# #####################################################################################	
	if tab == tab1 or tab == '':
		subreddit1 = 'Futurology'
		tab1 = Frame(nb)
		Frame(tab1, command=get_reddit_links(tab1,subreddit1, 8)).grid(row=4, column=1)
		nb.add(tab1, text='/r/'+subreddit1)
	
	if tab == tab2 or tab == '':
		subreddit2 = 'worldnews'
		tab2 = Frame(nb)
		Frame(tab2, command=get_reddit_links(tab2, subreddit2, 8)).grid(row=4, column=1)
		nb.add(tab2, text='/r/'+subreddit2)

	if tab == tab3 or tab == '':		
		subreddit3 = 'news'
		tab3 = Frame(nb)
		Frame(tab3, command=get_reddit_links(tab3, subreddit3, 8)).grid(row=4, column=1)
		nb.add(tab3, text='/r/'+subreddit3)
	
	if tab == tab4 or tab == '':	
		subreddit4 = 'entertainment'
		tab4 = Frame(nb)
		Frame(tab4, command=get_reddit_links(tab4, subreddit4, 8)).grid(row=4, column=1)
		nb.add(tab4, text='Other News')
		
	if tab == tab5 or tab == '':
		tab5 = Frame(nb)
		Frame(tab5, command=get_latest_PDS(tab5))
		nb.add(tab5, text='PDS & RS')
		w=Label(tab5, text="Latest RS News:", justify='left', font=15)
		w.grid(row=4, column=0)
		Frame(tab5,command=get_rs_news(tab5))
	# ######################################################################################
		
	if tab == '':	
		nb.pack(fill='both')
		img = PhotoImage(file=r'C:\Users\Riccardo\Desktop\Python Scripts\Personalized daily news\news-logo.gif')
		root.tk.call(('wm', 'iconphoto', root._w, img))
		#root.attributes('-alpha', 0.8) #Controls transparency
		
	time_now = time.time() - start_time
	print(time_now)

	root.mainloop()

if __name__ == '__main__':
	tab_default = ''
	tab1=tab2=tab3=tab4=tab5 = ''
	main(tab_default)
