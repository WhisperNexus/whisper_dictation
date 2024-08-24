# Whisper Dictation

Fast! Offline, privacy-focused, hands-free voice typing, AI voice chat, voice control, in **under 1 Gb of VRAM** when optimized for dictation alone. "The works" all AI features now running concurrently on a laptop with under 4 GiB of VRAM!

<img src="img/ss.png" alt="example pic" title="App does dictation anywhere, even social media." width="300" align="right">

- Listens and types quickly with `whisper-jax` or `whisper.cpp`,
- Hands-free, text appears under mouse cursor,
- Translates other languages into English,
- Launches & controls apps, with `pyautogui`,
- Optionally communicates with OpenAI `ChatGPT` or an included chat server.
- Optionally speaks answers out loud with `mimic3`.
- Draws pictures with stable-diffusion-webui.
- Client and server versions included.

**Freedoms and responsibilities** Free and open-source software comes with NO WARRANTIES. You have permission to copy and modify for individual needs in accordance with the included LICENSE. Download the updated project from https://github.com/themanyone/whisper_dictation.git

**The ship's computer.** Inspired by the *Star Trek* television series. Talk to your computer any time. And have it answer back with clear, easy-to-understand speech. Network it throughout the ship. Use your voice to write Captain's Log entries when the internet is down, when satellites are busy, or in the far reaches of the galaxy, "where no man has gone before."

**Privacy focused.** Most voice keyboards, dictation, translation, and chat bots depend on sending data to remote servers, which is a privacy concern. Keep data off the internet and confidential with your own, local servers. A CUDA-enabled video card with at least 1 Gb is all that's needed to run an uncensored virtual assistant that listens and responds via voice. While being completely free, offline, and independent.

**Dictation.** Start speaking and whatever you say will be pasted into the current window. This project now includes a couple clients. So other network users (even some phones and tablets that can run Linux) can use it without installing all these dependencies.

**Translation.** This app is optimized for dictation. It can do some translation into English. But that's not its primary task. To use it as a full-time translator, start whisper.cpp with `--translate` flag and use ggml-medium.bin or larger language model in place of ggml-small.en.bin.

Or if using JAX, set `task="transcribe"` to `task="translate"` inside `whisper_dictation.py`, and, if there is enough VRAM, choose a larger model for the pipeline, such as `openai/whisper-large-v2` for improved translation results.

**Voice control.** The bot also responds to commands.

For example, say, "Computer, search the web for places to eat". A browser opens up with a list of local restaurants. Say, "Computer, say hello to our guest". After a brief pause, there is a reply, either from `ChatGPT`, the included chat server on the local machine, or another, networked chat server that you set up. A voice, `mimic3` says some variation of, "Hello. Pleased to meet you. Welcome to our shop. Let me know how I can be of assistance". It's unique each time. Say, "Computer, open terminal". A terminal window pops up. Say "Computer, draw a picture of a Klingon warship". An image of a warship appears with buttons to save, print, and navigate through previously-generated images.

**AI Images.** Now with the included stable-diffusion API, `sdapi.py`, images may be generated locally, or across the network. Requires [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui). Start `webui.sh` on the server with --medvram or --lowvram and --api options. If using remotely, configure our `sdapi.py` client with the server's address.

**Chat.** You can converse with our own chat bot now. Start it with `flask run` whisper_dictation will use that. There is no need to say its name except to start the conversation. From then on it goes into a conversational mode. Say "Resume dictation" to start typing again.

Set the chat language model in `app.py`. The first time you use it, it will download the language model from huggingface. Our chat implementation keeps track of the current chat session only. The conversation is stored in RAM, and simply discarded after the program exits. It is never saved to the cloud, or made available to the Galactic Federation for the authorities at Star Fleet to go over with a fine-toothed comb...

## Advantages and trade-offs

**Security.** Older versions used a 10-minute audio buffer that stopped when it filled up. Now we recycle a tiny RAM buffer. Although this version can run continuously without filling up hard drives, there are valid concerns about letting it run unattended, because it can listen and also type commands. To prevent AI from taking over, *Please set screen saver to log out or lock the computer when not in use.* Or launch whisper_dictation with `timeout` utility to shut it off after a certain period of time.

**Whisper JAX or Whisper.cpp?** Whisper AI is currently the state of the art for open-source Python voice transcription software. [Whisper JAX](https://github.com/sanchit-gandhi/whisper-jax) accelerates Whisper AI with optimized JAX code. [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) takes a different route, and rewrites Whisper AI in bare-metal C++, so it might yield even better performance on some accelerated hardware. And, if you already have C++ development libraries, video drivers, tools, and experience, C++ eliminates having to download the roughly 5 GiB of Python dependencies for Whisper JAX.

Our implementation may be adapted to use any back-end implementation of Whisper AI. All we do is record audio when sound (hopefully speech) is detected. `whisper_dictation.py` transcribes the audio internally with `whisper-jax`, `whisper_client.py` sends it to a `whisper-jax` server. `whisper_cpp_client.py`, sends audio to an accelerated [Whisper.cpp](https://github.com/ggerganov/whisper.cpp), server you set up, or another audio transcription service.

The trade-off with running Whisper continuously is that some VRAM stays reserved until shutting down the stand-alone application or server. Depending on hardware and workflow, you might experience issues with other video-intensive tasks, games mostly, while these things are running.

For a simpler, light-weight, dictation-only client/server solution, try the [voice_typing](https://github.com/themanyone/voice_typing) app. It uses the bash shell to record and loads up whisper only when spoken-to. It now has a `whisper.cpp` thin client too. Or try the ancient, less-accurate [Freespeech](https://github.com/themanyone/freespeech-vr/tree/python3) project, which uses old-school Pocketsphinx, but is very light on resources.

Whisper Dictation is not optimized for making captions or transcripts of pre-recorded material. Use [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) or [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax) for that. They too have a [server with a web interface that makes transcripts for voice recordings and videos](https://github.com/sanchit-gandhi/whisper-jax/blob/main/app/app.py). If you want real-time AI captions translating everyone's conversations in the room into English. If you want to watch videos with accents that are difficult to understand. Or if you just don't want to miss what the job interviewer asked you during that zoom call... WHAT???, check out my other project, [Caption Anything](https://github.com/themanyone/caption_anything). And generate captions as you record live "what you hear" from the audio monitor device (any sounds that are playing through the computer).

## Whisper.cpp Client

We will need a few dependencies to get the `whisper.cpp` client running.

```shell
pip install ffmpeg
pip install pyautogui
pip install pyperclip
pip install pygobject
pip install openai
pip install requests
```

Now edit `whisper_cpp_client.py`, and set the address of cpp_url to the address of your server machine. In this case, it is already set up to use localhost.

`cpp_url = "http://127.0.0.1:7777/inference"`

## Whisper.cpp Server

Compile [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) with some type of acceleration for best results. We are using `cuBLAS`. Unfortunately, gcc versions later than 12 are not (currently) supported for building with `cuBLAS`*. If not using cuBLAS, you can follow whatever advice they have the Whisper.cpp docs and skip this section.

*TL-DR*. Our investigation has determined that the reason for `gcc-13` incompatibility is that `cuBLAS` libraries come pre-compiled with fixes for the [memcpy vs. memmove saga](https://www.win.tue.nl/~aeb/linux/misc/gcc-semibug.html) in glibc. The bug affected copying and moving memory (structs, pairs, and arrays which amount to what we call tensors). The `gcc-13` and `libstdc++13` tool chain now automatically attempts to fix the same bugs, so there is a conflict.

If you would like to experience this chaos for yourself, try using the unsupported compiler tool chain:
	`NVCCFLAGS="-allow-unsupported-compiler LLAMA_CUBLAS=1 make -j`

We now set up a `gcc-12` `conda` environment to keep things sane. We could also use a docker container for this.
```
conda create -n gcc12
conda activate gcc12
conda install -c conda-forge gxx=12
```

Since we intend to use this `gcc12` to build and install things for the host system, instead of just this conda environment, we will break it, by having it use the system `ld` and libraries. There might be a better way to do this, of which ignorance is bliss.
```
mv $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/lib64 $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/lib64.conda
ln -sf /usr/lib $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/
ln -sf /usr/lib64 $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/
ln -sf /usr/include $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/
ln -sf /usr/local $HOME/.conda/envs/gcc12/x86_64-conda-linux-gnu/sysroot/
```

The Makefile expects `cuda` to be installed in `/opt/cuda`
```
sudo ln -s /etc/alternatives/cuda /opt/cuda
```

And, after installing the package which provides `/usr/lib64/libpthread_nonshared.a` (`compat-libpthread-nonshared`), we can build with `cuBLAS`.

```
cd whisper.cpp
git pull
conda activate gcc12
WHISPER_CUBLAS=1 make -j
```

If you didn't break your conda environment like we did, ignore errors "local/cuda/lib64/libcublas.so: undefined reference to `memcpy@GLIBC_2.14'"
If there were errors, re-run make outside of conda to finish linking using the system `ld` and libraries. See what we did there?

```
conda deactivate
WHISPER_CUBLAS=1 make -j
./whisper.cpp -l en -m ./models/ggml-tiny.en.bin samples/jfk.wav`
```

To minimize GPU footprint, use the tiny.en model. It consumes just over 111 MiB VRAM on our budget laptop. 48MiB with `./models/ggml-tiny.en-q4_0.bin` quantized to 4 Bits.  `--convert` is no longer required since we started using wav files instead of `.mp3` which whisper.cpp ffmpeg is having difficulty with lately. We started using port 7777 because 8080 is used by other apps. Feel free to change it. As long as servers and clients agree, it should be no problem.

We launch `server` under the name, `whisper_cpp_server` to make it less confusing when it shows up in the process list.
```shell
ln -sf $(pwd)/main whisper_cpp
ln -sf $(pwd)/server whisper_cpp_server
./whisper_cpp_server -l en -m models/ggml-tiny.en.bin --port 7777
```

Earlier versions of this document said you could compile with `gcc13`, and then add the `-ng` flag, but that cuts performance in half, compared with using `gcc12` and getting a full CUDA build.

If `whisper_cpp_server` refuses to start, reboot. Or, especially if using the unsupported compiler like we did, reload the crashed NVIDIA uvm module `sudo modprobe -r nvidia_uvm && sudo modprobe nvidia_uvm`. Hopefully this will no longer be necessary, but you never know. So we are leaving it here. We are crazy hackers now, aren't we.

Edit `whisper_cpp_client.py` clients to change the server location from localhost to wherever the server resides on the network.

**Start a client.**

```shell
cd whisper_dictation
./whisper_cpp_client.py
```

**Optionally start a chat server.**

```shell
flask run
```

**Optionally start stable-diffusion webui**

```shell
webui.sh --api --medvram
```

Control your computer. Refer to the section on [spoken commands and program launchers](#Spoken).

## Client / Server dependencies

Install some things to make the python apps work.

```shell
sudo dnf install python-devel gobject-introspection-devel python3-gobject-devel cairo-gobject-devel python3-tkinter python3-devel
pip install ffmpeg
pip install pyautogui
pip install pyperclip
pip install pygobject
pip install --upgrade onnxruntime==1.15.1
```

## Whisper-JAX Setup and dependencies

If not using `whisper.cpp`, or to compare back ends, we can also connect to Whisper-JAX.

Go to https://github.com/google/jax#installation and follow through the steps to install cuda, cudnn, or whatever is missing. All these [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax) dependencies and video drivers can be quite bulky, requiring about 5.6 GiB of downloads.

Install `torch` nightly version for the chat server. It may be a challenge to install it in the same conda or venv virtual environment as `whisper_dictation`. We just install everything to the main python installation now. With an earlier version of `torch`, it would downgrade `nvidia-cudnn-cu11` to an incompatible version. Then it was necessary to run something like `./.venv/bin/python -m pip install --upgrade nvidia-cudnn-cu11` from within the virtual environment to make `whisper-jax` work again. It works now with the following install commands. Or you can try building `torch` from source. You still might be easier to use conda or venv to keep things separate.

The commands to install JAX for GPU(CUDA) are copied [from here](https://jax.readthedocs.io/en/latest/index.html).

Install [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax) and make sure the examples work. You may need to reboot to properly initialize accelerated drivers, e.g. CUDA, after getting everything installed. And after each kernel update, and video driver upgrade/recompilation. An alternative to rebooting is to reload the module responsible for acceleration. For Nvidia, `sudo modprobe -r nvidia_uvm && sudo modprobe nvidia_uvm`.

```shell
# activate conda or venv (optional)
python3 -m venv .venv
source .venv/bin/activate
# install dependencies (links may need updating someday)
pip install --upgrade onnxruntime==1.15.1
pip install numpy
pip install  nvidia-cudnn-cu11
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu123
pip install --upgrade --no-deps --force-reinstall git+https://github.com/sanchit-gandhi/whisper-jax.git
pip install --upgrade transformers>=4.27.4
#GPU https://github.com/google/jax?tab=readme-ov-file#installation
pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
#Or TPU
pip install -U "jax[tpu]" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

There may be other dependencies. Look in requirements.txt.

Modify `dictate.py` and set the preferred threshold audio level and device. This could require experimentation. If the microphone is not detected, open Control Center or Volume Control settings. And choose the preferred audio device for the mic, whether it is a Bluetooth, USB microphone, or whatever. You can also use `gst-inspect-1.0` to get a list of audio sources to try. The default `autoaudiosrc` should work in most cases. 

Again, explore the examples on the [Whisper-Jax](https://github.com/sanchit-gandhi/whisper-jax) page and make sure whisper is working first. Edit `whisper_dictation.py` to use the preferred pipeline and dictation model from their examples for best results. We found that `jnp.bfloat16` is for TPU devices. So `jnp.float16` is what we use for our laptop GPU. Those with a decent, desktop GPU might prefer float32. Reference, [PyTorch docs.](https://pytorch.org/xla/release/2.1/index.html)

Now we are ready to try dictation.

## Usage

```shell
cd whisper_dictation
./whisper_dictation.py
```

Refer to the section on [GPU memory usage](#Issues).

If it complains about missing files, modify `whisper_dictation.py` and, in the first line, set the location of Python to the one inside the virtual environment that works with Whisper-JAX. The one you installed everything in. The default for our usage is `.venv/bin/python` which should load the correct one. But if it doesn't, you can change this to the path of python inside the conda or venv environment. Then you don't have to source or activate the virtual environment each time. You can just change to the directory and run it.

Feel free to change the FlaxWhisperPipline language, or use "openai/whisper-large-v2" if your video card can afford having more than 1Gb VRAM tied-up. It defaults to `openai/whisper-small.en` which uses around 975 MiB VRAM when [optimized for size](#Issues). But in fact, we get *fantastic* results even with `openai/whisper-tiny.en` So you might want to go tiny instead. Then it might even work with a tiny video card.

### Spoken commands and program launchers

The computer responds to commands. You can also call him Peter.

**Mute button.** There is no mute button. Say "pause dictation" to turn off text generation. It will keep listening to commands. Say "resume dictation", or "Computer, type this out" to have it start typing again. Say "stop listening" or "stop dictation" to quit the program entirely. You could configure a button to mute your mic, but that is no longer necessary and beyond the scope of this program.

These actions are defined in whisper_dictation.py. See the source code for the full list. Feel free to edit them too!

Try saying:
- Computer, open terminal.
- Computer, go to [thenerdshow.com](https://thenerdshow.com/). (or any website).
- Computer, open a web browser. (opens the default homepage).
- Computer, show us a picture of a Klingon battle cruiser.
- Page up.
- Page down.
- Undo that.
- Copy that.
- Paste it.
- Pause dictation.
- Resume dictation.
- New paragraph. (also submits chat forms :)
- Peter, tell me about the benefits of relaxation.**
- Peter, compose a Facebook post about the sunny weather we're having.
- Stop dictation. (quits program).

** export your OPENAI_API_KEY to the environment if you want answers from ChatGPT. If your firm is worried about privacy and security, use the local chat bot with `flask run` or `llama.cpp` as explained below. ChatGPT also has an enterprise version that they claim to be more private and secure. We are not affiliated with OpenAI, and therefor do not receive referral benefits.

### Optional chat and text-to-speech

```shell
# in another terminal, not using the .venv reserved for whisper_dictation
pip install "accelerate>=0.16.0,<1" "transformers[torch]>=4.28.1,<5" "torch>=1.13.1,<2"
cd whisper_dictation
flask run
```

```shell
export OPENAI_API_KEY=<my API key>
```

If there is no API key, or if ChatGPT is busy, it will ping a private language model running on http://localhost:5000. There are language models on [huggingface](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) that produce useful results with < 4GiB of video RAM. So now whisper_dictation has its own, privacy-focused chat bot. Edit `app.py` and choose a larger language model if your system supports it.

# Run a powerful chatbot locally

Having the included chat bot talk back is novel, but it can be a pain with long answers. What you *really* want, for the best mix of privacy and knowledge power, is to install [llama.cpp](https://github.com/ggerganov/llama.cpp). An older version of `llama.cpp` is bundled with [GPT4All](https://github.com/nomic-ai/gpt4all) but we don't need all that. 

## Get llama.cpp working

Compile [llama.cpp](https://github.com/ggerganov/llama.cpp) with some type of acceleration as indicated in their docs. We compile with CUDA after installing nvidia drivers and openBLAS.

If you followed our instructions for compiling `whisper.cpp` with `cuBLAS`, you should be all set to compile `llama.cpp`. Again, if not using cuBLAS, skip this section.

```
conda activate gcc12
GGML_CUDA=1 make -j
```

Or in our particular case...
```
conda activate gcc12
LLAMA_FAST=1 LLAMA_CUDA_F16=1 LLAMA_CUDA=1 make -j 8
conda deactivate
LLAMA_FAST=1 LLAMA_CUDA_F16=1 LLAMA_CUDA=1 make -j 8
```

## Download a language model

For a good, small languag model, try [the ones on our page](https://huggingface.co/hellork). Look at the [leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) to see which models are the best that can fit into your VRAM. Then search for the model in .gguf format. To save VRAM and time, download the quantized models, or [quantize them here](https://huggingface.co/spaces/ggml-org/gguf-my-repo). We were able to run a quantized gemma-2 (2B) with all layers loaded (-ngl 27) on 2GiB VRAM. Larger 7B models can only load a few layers (-ngl 16), perform slowly, and we have to close other applications. (Or we can quantize them to 3 bits with a noticeable loss in quality).

## Start chatting

Run chat in interactive mode, in the terminal, using Whisper Dictation to type questions. It won't speak its answers. But you won't have to listen to pages and pages of response text, either. But you could also restrict the number of response tokens (-n).

And just like that. We can explore the results of months of researching "What's the best AI that I can realistically use on my laptop?" The future is here! Use `-ngl` option for maximum warp. Launch codes:

`./llama-cli -ngl 27 -m models/gemma-2-2b-it-q4_k_m.gguf --multiline-input --color --interactive-first -p "You are a helpful and knowledgeable assistant.`

## Give it a voice

**Mimic3.** If you install [mimic3](https://github.com/MycroftAI/mimic3) as a service, the computer will speak answers out loud. Follow the [instructions for setting up mimic3 as a Systemd Service](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mimic-tts/mimic-3#web-server). The `mimic3-server` is already lightening-fast on CPU. Do not bother with --cuda flag, which requires old `onnxruntime-gpu` that is not compatible with CUDA 12+ and won't compile with nvcc12... We got it working! And it just hogs all of VRAM and provides no noticeable speedup anyway. Regular `onnxruntime` works fine with mimic3.

**Female voice.** For a pleasant, female voice, use  `mimic3-download` to obtain `en_US/vctk_low` and change the `params` line in `mimic3_client`, commenting the other line out, like so:

```
    # params = { 'text': text, "lengthScale": "0.6" }
    params = { 'text': text, "voice": "en_US/vctk_low" }
```

# Files in this project

`whisper_cpp_client.py`: A small and efficient Python client that connects to a running [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) server on the local machine or across the network.

`whisper_dictation.py`: A stand-alone app bundled with Whisper-JAX Python. (No server required.) It loads the language model and takes a long time to start up. It also uses more VRAM (adjustable with environment variables. See JAX documentation). But with those extra resources it might be more responsive than client/server solutions.

`whisper_client.py`: A client version of Whisper Dictation. The client connects to a local [Whisper JAX server](https://jserver.py) running on the machine, the local network, or the internet. Edit `whisper_client.py` to configure the server location. Clients make dictation available even on budget laptops and old phones that can run linux/python from the app store.

`jserver.py`: A `whisper-jax` server. Run it with `venv-run jserver.py`. You might also find that, although they start quickly, clients are slightly less-responsive, compared to the bundled version. This is because servers set aside extra resources to handle multiple clients, resources which typically aren't necessary for one user. If only a handful of clients will use it, editing `jserver.py` in certain ways may speed it up somewhat. Make it use the "openai/whisper-tiny.en" checkpoint. Reduce BATCH_SIZE, CHUNK_LENGTH_S, NUM_PROC to the minimum necessary to support your needs.

`record.py`: A sound-activated recorder for hands-free recording from the microphone. It waits up to 10 minutes listening for a minimum threshold sound level of, -20dB, but you can edit the script and change that. It stops recording when audio drops below that level for a couple seconds. You can run it separately. It creates a cropped audio soundbite named `audio.mp3`. Or you can supply an output file name on the command line.

`app.py`: A local, privacy-focused AI chat server. Start it by typing `flask run` from within the directory where it resides. You can use almost any chat model on huggingface with it. Edit the file, and and change the model configuration. It is not a security-focused server, however. So beware using it outside the local network. And do not share its address with more than a few friends. In particular, flask apps have no built-in protection against distributed denial-of-service attacks (DDoS).

Various test files, including:

`mimic3_client.py`: a client to query and test `mimic3-server` voice output servers.

`test_cuda.py`: test your torch, pytorch, cuda, and optional onnxruntime installation

### Improvements

**Stable-Diffusion.** Stable-Diffusion normally requires upwards of 16 GiB of VRAM. But we were able to get it running with a mere 2 GiB using the `--medvram` or `--lowvram` option with [The Stable Diffusion Web UI](https://techtactician.com/stable-diffusion-low-vram-memory-errors-fix/). 

**Text goes to wrong place.** We now use `pyperclip` and `pyautogui` to paste text, instead of typing responses into the current window. We use middle-click paste on Linux, so that it also works in terminals. If you miss and it doesn't put text where you want, you can always manually middle-click it somewhere else.

**Fixing Linux paste.** "No. I don't want to use middle-click on Linux!" The alternative to faking middle click on Linux is to change the behavior of the Linux terminal. Are you tired of having to remember to use Ctrl-Shift-C and Ctrl-Shift-V in the terminal, instead of Ctrl-C and Ctrl-V? The beauty of Linux is being able to customize. So let's do it!

[Modifying Terminal Settings](https://askubuntu.com/questions/53688/making-ctrlc-copy-text-in-gnome-terminal)

    Open your terminal emulator (e.g., gnome-terminal, xterm, etc.).
    Go to the terminal's menu and select "Edit" or "Preferences".
    Look for the "Shortcuts" or "Keyboard" section.
    Find the entry for "Copy" or "Interrupt" and modify the keybinding from CTRL-Shift-C to CTRL-C. Do the same for CTRL-Shift-V, changing it to CTRL-V.
    The interrupt or "stop script" hotkey will automatically be remapped from CTRL-C to Ctrl-Shift-C.
        Note: The exact steps may vary depending on your terminal emulator. Refer to the above link or help resources specific to your terminal emulator for more information.

By following these steps, you will have swapped the behavior of the "break" or "stop script" Ctrl-C, and the copy, Ctrl-Shift-C hotkeys in the Linux terminal.

Now we are ready to change `whisper_cpp_client.py`, `whisper_dictation.py` or `whisper_client.py` to use Ctrl-V paste instead of middle click. Somewhere around line 144, change the line that says `pyautogui.middleClick()` to `pyautogui.hotkey('ctrl', 'v')`.

**I want it to type slowly.** We would love to have it type text slowly, but typing has become unbearably-slow on sites like Twitter and Facebook. The theory is they are using JavaScript to restrict input from bots. But it is annoying for fast typists too. If occasional slow typing doesn't bother you, change the code to use `pyautogui.typewrite(t, typing_interval)` for everything, and set a `typing_interval` to whatever speed you want.

## JAX Issues

**GPU memory usage.** According to [JAX documentation](https://jax.readthedocs.io/en/latest/gpu_memory_allocation.html), JAX pre-allocates around 75% of VRAM to reduce allocation overhead and memory fragmentation. Configure JAX GPU usage through environment variables to save space.

`export XLA_PYTHON_CLIENT_ALLOCATOR=platform` provides the smallest GPU footprint, 983 MiB with `openai/whisper-small.en`. We noticed no performance penalty, and no memory fragmentation with this setting. Because Whisper Dictation only uses one compiled JAX process, and reuses it each time. Put in `~/.bashrc` or `~/.bash_profile` to make changes persistent.

If the above setting causes problems, try the following.

`export XLA_PYTHON_CLIENT_PREALLOCATE=false` This uses around 2048 MiB of VRAM. We did not notice *any* performance boost pre-allocating half of our laptop's VRAM. But mileage may vary.

`export XLA_PYTHON_CLIENT_MEM_FRACTION=.XX` If the above pre-allocation is enabled, this makes JAX pre-allocate XX% of the total GPU memory, instead of the default 75%.

Monitor JAX memory usage with [jax-smi](https://github.com/ayaka14732/jax-smi), `nvtop`, `nvidia-smi`, or by installing the bloated, GreenWithEnvy (gwe) from Nvidia that does the exact-same thing with a graphical interface.

This is a fairly new project. There are bound to be more issues. Share them on the [issues section on GitHub](https://github.com/themanyone/whisper_dictation/issues). Or fork the project, create a new branch with proposed changes. And submit a pull request.

### Thanks for trying out Whisper Dictation!

Browse Themanyone
- GitHub https://github.com/themanyone
- YouTube https://www.youtube.com/themanyone
- Mastodon https://mastodon.social/@themanyone
- Linkedin https://www.linkedin.com/in/henry-kroll-iii-93860426/
- [TheNerdShow.com](http://thenerdshow.com/)
