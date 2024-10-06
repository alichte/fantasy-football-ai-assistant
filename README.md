# Fantasy Football AI Assistant

## What Can It Do? 
Tired of having to sort through multiple different ESPN Fantast Football leagues, doing the same tedious tasks every day? Me too. 

This notebook and the accompanying set of functions/tools in `espn_ff_toolkit` aim to give you some assistance with the worst parts of fantasy football. Using the code here, you can stand up a smart assistant that will check your roster across multiple leagues and check available free agents in all leagues. It has access to Google, to check for any recent news about your players and free agents. 

## What You Need to Run
You'll need to bring your own API keys to the table. Set environment variables for `OPENAI_API_KEY`, `GOOGLE_API_KEY`,`GOOGLE_CSE`,`ESPN_S2`. and `ESPN_SWID`. There is documentation through OpenAI, Google, and the `espn_api` package that can help you track all of these down if you've never done it before. 

## How to Use
The dashboard can be run either directly from the app folder by using `streamlit run app.py` or by building an image from the dockerfile and deploying.

## Coming Soon
Coming soon: Checking recent league activity, checking ESPN injury status
