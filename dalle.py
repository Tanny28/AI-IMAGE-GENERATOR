from tkinter import *
import customtkinter 
from tkinter import messagebox
from tkinter import filedialog
import openai

from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import pickle



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#APP
root = customtkinter.CTk()
root.title("AI Image Gen By Tanmay Shinde")
root.geometry('700x300')

#GRAB KEY 
def grab_key():
	#DEFINE FILENAME
	filename ='api_key'
	try:
		if os.path.isfile(filename):
			#OPEN FILE
			input_file = open(filename,'rb')
			#LOAD DATA IN VAR
			stuff = pickle.load(input_file)
			#OUTPUT STUFF
			return stuff
		else:
			#CREAT FILE 
			input_file= open(filename,'wb')
			#CLOSE
			input_file.close()
	except Exception as e:
		messagebox.showinfo("WHOOPS!!",f'Error: {e}')	
		


#SAVE API KEY FUNCTION
def save_key():
	#CREATE NEW WINDOW
	api_window = customtkinter.CTkToplevel(root)
	api_window.title("API KEY")
	api_window.geometry("500x300")

	def saver():
		#DEFINE FILENAME
		filename ='api_key'
		try:
			#OPEN FILE
			output_file = open(filename,'wb')

			#ADD STUFF
			pickle.dump(api_entry.get(), output_file)
			messagebox.showinfo("Saved!","Your API Key was saved!!") 
			#CLOSE WIN
			api_window.destroy()
			api_window.update()

		except Exception as e:
			messagebox.showinfo("WHOOPS!!",f'Error: {e}')
	
	def get_key():
		#DEFINE FILENAME
		filename ='api_key'
		try:
			if os.path.isfile(filename):
				#OPEN FILE
				input_file = open(filename,'rb')
				#LOAD DATA IN VAR
				stuff = pickle.load(input_file)
				#OUTPUT STUFF
				api_entry.insert(0,stuff)
			else:
				#CREAT FILE 
				input_file= open(filename,'wb')
				#CLOSE
				input_file.close()







		except Exception as e:
		  messagebox.showinfo("WHOOPS!!",f'Error: {e}')	

			

	#LABLE
	api_label = customtkinter.CTkLabel(api_window,text="API Key",font=("Helvetica", 18))
	api_label.pack(pady=20)

	#ADD ENTRY BOX
	api_entry =customtkinter.CTkEntry(api_window,width=300)
	api_entry.pack(pady=10)

	#ADD BUTTON
	save_api_button = customtkinter.CTkButton(api_window, text="Save Key",command=saver)
	save_api_button.pack(pady=10)

	#GET KEY
	get_key()





#FUNCTION 
def generate():
	#TEXT FROM BOX 
	prompt = my_text.get("0.0","end") 
	#SIZE OPTION
	size = radio_var.get()

	#SURE WE TYPE SOMETHING 
	if my_text.compare("end-1c","==","1.0"):
		messagebox.showinfo("Whoops!","Please Type something !")
	else:
		try:
			#API KEY
			key =grab_key()
			#openai.api_key='sk-proj-vFNuhhOY2GxfGF8veUgXT3BlbkFJvskQE7ItMXfW1fWUoFyI'
			openai.api_key = key

			#RESPONSE
			response= openai.Image.create(prompt=prompt, n=1, size=f'{size}x{size}')
			#GET URL
			image_url = response['data'][0]['url']

			#NEW WINDOW
			new_window = customtkinter.CTkToplevel(root)
			new_window.title(f'{size}x{size}')
			new_window.geometry(f'{size}x{size}')

			def copy_url():
				#CLEAR CLIPB
				new_window.clipboard_clear()
				#COPY TO CLIPB
				new_window.clipboard_append(image_url)
				#SUCC MESSAGE
				messagebox.showinfo("Copied!","Your URL has been copied successfully!")

			

			def save_image():
			    file_name = filedialog.asksaveasfilename(initialdir="C:/dalle/images",
			    	title="Save Image",
			    	filetypes=(("PNG Files","*.png"),("All Files", "*.*")))  

			    if file_name:
			    	#FILENAME ENDS WITH PNG
			    	if file_name.endswith(".png"):
			    		pass

			    	else:
			    		file_name = f"{file_name}.png"
			    	#SAVE FILE 
			    	save_image =Image.open(BytesIO(img_data)).save(file_name)	
			    	messagebox.showinfo("Saved!","Your image has been Saved!!")



			    else:
			    	messagebox.showinfo("Whoops!","You Forgot to Enter A File Name,Please Try Again.")


			    	 

			#ADD MENU
			my_menu = Menu(new_window)
			optionbar = Menu(my_menu, tearoff=0)
			optionbar.add_command(label="Copy URL", command= copy_url)
			optionbar.add_command(label="Save Image", command=save_image)

			my_menu.add_cascade(label="File", menu=optionbar)
			new_window.config(menu=my_menu)


			#ADD IMAGE 
			response_image = requests.get(image_url)
			img_data = response_image.content
			img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
			#ADD LABLE IN NEW WINDOW
			panel = customtkinter.CTkLabel(new_window,	image=img, text='')
			panel.pack(side="bottom",fill="both", expand='yes')
			# DELETE FROM TEXT BOX
			my_text.delete('0.0', 'end')
		except Exception as e:
			#DELETE FROM TEXTBOX
			#my_text.delete('0.0','end')
			#INSERT ERROR MESSAGE
			#my_text.insert("end",e)

			#POP ERROR MESS
			messagebox.showinfo("OpenAi Error", f'{e}')


			


#TEXTBOX
my_text = customtkinter.CTkTextbox(root,width=650,height=200)
my_text.pack(pady=10)

#FRAME BUTTONS
my_frame = customtkinter.CTkFrame(root)
my_frame.pack()

#RADIO BUTTONS 
radio_var = customtkinter.IntVar(value=256)
rb1 = customtkinter.CTkRadioButton(my_frame, text="256x256",variable=radio_var,value=256)
rb2 = customtkinter.CTkRadioButton(my_frame, text="512x512",variable=radio_var,value=512)
rb3 = customtkinter.CTkRadioButton(my_frame, text="1024x1024",variable=radio_var,value=1024)

#BUTTON ON SCREEN
rb1.grid(row=0,column=0)
rb2.grid(row=0,column=1)
rb3.grid(row=0,column=2)



#ADD FRAME 
my_frame = customtkinter.CTkFrame(root)
my_frame.pack(pady=10)


#MAIN BUTTON
my_button = customtkinter.CTkButton(my_frame,text="Generate Image",command=generate)
my_button.grid(row=0, column=0, padx=10)

api_button = customtkinter.CTkButton(my_frame, text="API Key",command=save_key)
api_button.grid(row =0,column= 1)







root.mainloop()