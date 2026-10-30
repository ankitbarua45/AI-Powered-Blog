from fastapi import APIRouter, Depends, HTTPException
from models.schemas import AISuggestionRequest, AISuggestionResponse, AITextRewriteRequest, AITextRewriteResponse
from models.database import settings
from routers.auth import get_current_user, User
from openai import OpenAI
from typing import List
from openai import AuthenticationError, RateLimitError

router = APIRouter()

# Initialize OpenAI client with cost-effective model
client = OpenAI(api_key=settings.OPENAI_API_KEY)
MODEL = settings.OPENAI_MODEL  # Using gpt-4o-mini by default (small, low-power, cost-effective)

@router.post("/suggestions", response_model=AISuggestionResponse)
async def get_ai_suggestions(
    request: AISuggestionRequest,
    current_user = Depends(get_current_user)
):
    try:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj") and len(settings.OPENAI_API_KEY) < 50:
            # Return mock suggestions if API key is invalid
            return AISuggestionResponse(
                suggestions=[
                    "Start with an engaging introduction",
                    "Add 3-5 main sections with clear headings",
                    "Include examples and practical tips",
                    "Add a compelling conclusion with call-to-action",
                    "Use bullet points for better readability"
                ],
                type=request.suggestion_type
            )

        prompt = f"""
        You are an expert blog content writer. The user wants to write a blog post about: "{request.topic}"
        
        Please provide {request.suggestion_type} suggestions for this topic.
        
        {"Additional context: " + request.context if request.context else ""}
        
        Format your response as a numbered list of suggestions.
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful blog content assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        content = response.choices[0].message.content
        
        # Parse the suggestions
        suggestions = []
        for line in content.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering/bullets
                clean_line = line.split('.', 1)[-1].strip() if '.' in line else line[1:].strip()
                if clean_line:
                    suggestions.append(clean_line)

        return AISuggestionResponse(
            suggestions=suggestions,
            type=request.suggestion_type
        )

    except RateLimitError:
        # Return mock suggestions if out of credits
        return AISuggestionResponse(
            suggestions=[
                "Start with an engaging introduction",
                "Add 3-5 main sections with clear headings",
                "Include examples and practical tips",
                "Add a compelling conclusion with call-to-action",
                "Use bullet points for better readability"
            ],
            type=request.suggestion_type
        )
    except AuthenticationError:
        # Return mock suggestions if auth fails
        return AISuggestionResponse(
            suggestions=[
                "Start with an engaging introduction",
                "Add 3-5 main sections with clear headings",
                "Include examples and practical tips",
                "Add a compelling conclusion with call-to-action",
                "Use bullet points for better readability"
            ],
            type=request.suggestion_type
        )
    except Exception as e:
        print(f"AI Suggestions Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating AI suggestions: {str(e)}")

@router.post("/rewrite", response_model=AITextRewriteResponse)
async def rewrite_text(
    request: AITextRewriteRequest,
    current_user = Depends(get_current_user)
):
    try:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj") and len(settings.OPENAI_API_KEY) < 50:
            # Return original text with slight improvements if API key is invalid
            improved_text = request.text.strip()
            # Simple improvements
            improved_text = improved_text.replace("  ", " ")  # Remove double spaces
            improved_text = improved_text.replace("..", ".")  # Fix double periods
            
            return AITextRewriteResponse(
                rewritten_text=improved_text,
                original_text=request.text
            )

        rewrite_instructions = {
            "improve": "Improve the writing quality, clarity, and flow while maintaining the original meaning.",
            "shorten": "Make the text more concise while keeping the key information.",
            "expand": "Expand the text with more details and examples.",
            "formal": "Rewrite in a more formal, professional tone.",
            "casual": "Rewrite in a more casual, conversational tone."
        }

        instruction = rewrite_instructions.get(request.rewrite_type, rewrite_instructions["improve"])

        prompt = f"""
        Please rewrite the following text to {instruction}.
        
        Original text: "{request.text}"
        
        {"Additional context: " + request.context if request.context else ""}
        
        Provide only the rewritten text, no explanations.
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful writing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )

        rewritten_text = response.choices[0].message.content.strip()

        return AITextRewriteResponse(
            rewritten_text=rewritten_text,
            original_text=request.text
        )

    except RateLimitError:
        # Return basic improvements if out of credits
        improved_text = request.text.strip()
        improved_text = improved_text.replace("  ", " ")
        improved_text = improved_text.replace("..", ".")
        
        return AITextRewriteResponse(
            rewritten_text=improved_text,
            original_text=request.text
        )
    except AuthenticationError:
        # Return basic improvements if auth fails
        improved_text = request.text.strip()
        improved_text = improved_text.replace("  ", " ")
        improved_text = improved_text.replace("..", ".")
        
        return AITextRewriteResponse(
            rewritten_text=improved_text,
            original_text=request.text
        )
    except Exception as e:
        print(f"AI Rewrite Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error rewriting text: {str(e)}")

@router.post("/generate-outline")
async def generate_outline(
    topic: str,
    current_user = Depends(get_current_user)
):
    try:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-proj") and len(settings.OPENAI_API_KEY) < 50:
            # Return a mock outline if API key is invalid
            outline = f"""
# {topic}

## Introduction
- Hook the reader with an interesting opening
- Briefly explain what the post will cover
- Set expectations for the reader

## Main Content
### Section 1: Understanding the Basics
- Define key concepts
- Explain why this topic matters
- Provide foundational knowledge

### Section 2: Practical Applications
- Show real-world examples
- Provide step-by-step guidance
- Include tips and best practices

### Section 3: Advanced Techniques
- Go beyond the basics
- Discuss complex scenarios
- Share expert insights

## Conclusion
- Summarize key points
- Provide actionable next steps
- End with a strong call-to-action
"""
            return {"outline": outline}

        prompt = f"""
        Create a detailed blog post outline for the topic: "{topic}"
        
        The outline should include:
        - An engaging introduction
        - 3-5 main sections with sub-points
        - A compelling conclusion
        
        Format as a structured outline with clear hierarchy.
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert blog content writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )

        outline = response.choices[0].message.content

        return {"outline": outline}

    except RateLimitError:
        # Return mock outline if out of credits
        outline = f"""
# {topic}

## Introduction
- Hook the reader with an interesting opening
- Briefly explain what the post will cover
- Set expectations for the reader

## Main Content
### Section 1: Understanding the Basics
- Define key concepts
- Explain why this topic matters
- Provide foundational knowledge

### Section 2: Practical Applications
- Show real-world examples
- Provide step-by-step guidance
- Include tips and best practices

### Section 3: Advanced Techniques
- Go beyond the basics
- Discuss complex scenarios
- Share expert insights

## Conclusion
- Summarize key points
- Provide actionable next steps
- End with a strong call-to-action
"""
        return {"outline": outline}
    except AuthenticationError:
        # Return mock outline if auth fails
        outline = f"""
# {topic}

## Introduction
- Hook the reader with an interesting opening
- Briefly explain what the post will cover
- Set expectations for the reader

## Main Content
### Section 1: Understanding the Basics
- Define key concepts
- Explain why this topic matters
- Provide foundational knowledge

### Section 2: Practical Applications
- Show real-world examples
- Provide step-by-step guidance
- Include tips and best practices

### Section 3: Advanced Techniques
- Go beyond the basics
- Discuss complex scenarios
- Share expert insights

## Conclusion
- Summarize key points
- Provide actionable next steps
- End with a strong call-to-action
"""
        return {"outline": outline}
    except Exception as e:
        print(f"Error generating outline: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating outline: {str(e)}")
