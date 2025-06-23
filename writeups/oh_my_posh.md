Beautify Terminal with Oh My Posh
In this post, I'll walk you through setting up Oh My Posh on a Linux system. It's a prompt theme engine for any shell that helps make your terminal not just more visually appealing- but also more informative.

### Oh My Posh  

Oh My Posh isn't just about looks - it helps improve terminal productivity with context-aware prompts, git status indicators, and more.  

##### 🔧 Step 1: Install Oh My Posh  

To get started, open your terminal and run the following command:  
`curl -s https://ohmyposh.dev/install.sh | bash -s`  

This script will download and install Oh My Posh to your system. By default, it gets installed to:  

`/home/<your-username>/.local/bin`  

[!NOTE] Make sure this location is included in your PATH.  

##### 🛠 Step 2: Add Oh My Posh to Your Shell Path  

Depending on your shell (e.g., bash or zsh), add the path to your configuration file so the shell can access the oh-my-posh binary.  

For Bash:  

```sh
Edit your ~/.bashrc file:
export PATH=$PATH:/home/<your-username>/.local/bin
```  

For Zsh:

```sh
Edit your ~/.zshrc file:
export PATH=$PATH:/home/<your-username>/.local/bin
```  

💡 Replace <your-username> with your actual Linux username.  

```sh
After editing, apply the changes:
source ~/.bashrc
# or
source ~/.zshrc
```  

##### 🎨 Step 3: Install a Nerd Font  

Oh My Posh requires a Nerd Font to render all the icons and symbols correctly. The easiest way to install one is:  

`oh-my-posh font install meslo`  

Meslo is a great choice and widely used. After installation, be sure to set your terminal to use the MesloLGS NF font in its preferences.  

##### 📁 Step 4: Create a Directory for Your Theme  

Let's store your theme config in a safe place:  

`mkdir -p ~/posh/theme`    

Place your .omp.json theme file (e.g., easy-term.omp.json) in that directory.  

##### ⚙️ Step 5: Activate Oh My Posh  
Now, let's initialize Oh My Posh with your theme.  

For Bash:  

Add this to the end of your ~/.bashrc:

`eval "$(oh-my-posh init bash --config '/home/<your-username>/posh/theme/easy-term.omp.json')"`  

For Zsh:  

Add the equivalent to your ~/.zshrc:  

`eval "$(oh-my-posh init zsh --config '/home/<your-username>/posh/theme/easy-term.omp.json')"`   

Then, apply the changes:  

```sh
source ~/.bashrc  
# or  
source ~/.zshrc
```  

##### ✅ Done  

Now open a new terminal window and enjoy your stylish new prompt!  
Just adjust the paths to match your environment.  


[![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*jmegqwTOXxIPhOH8-BwQCA.png)]

Sayonara :)
