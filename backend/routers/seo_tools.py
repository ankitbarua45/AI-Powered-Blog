from fastapi import APIRouter, Depends, HTTPException
from models.schemas import SEOAnalysisRequest, SEOAnalysisResponse
from routers.auth import get_current_user, User
from typing import List, Dict
import re
from bs4 import BeautifulSoup
import markdown

router = APIRouter()

def analyze_title(title: str, target_keywords: List[str]) -> Dict:
    """Analyze the blog post title for SEO."""
    issues = []
    score = 100
    
    # Length check
    if len(title) < 30:
        issues.append("Title is too short (under 30 characters)")
        score -= 15
    elif len(title) > 60:
        issues.append("Title is too long (over 60 characters)")
        score -= 10
    
    # Keyword presence
    title_lower = title.lower()
    keywords_found = [kw for kw in target_keywords if kw.lower() in title_lower]
    
    if target_keywords and not keywords_found:
        issues.append("Title doesn't contain any target keywords")
        score -= 20
    elif len(keywords_found) < len(target_keywords) / 2:
        issues.append("Title contains fewer than half of target keywords")
        score -= 10
    
    return {
        "score": max(0, score),
        "issues": issues,
        "keywords_found": keywords_found
    }

def analyze_content(content: str, target_keywords: List[str]) -> Dict:
    """Analyze the blog post content for SEO."""
    issues = []
    score = 100
    
    # Convert markdown to HTML for analysis
    html_content = markdown.markdown(content)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text
    text = soup.get_text()
    word_count = len(text.split())
    
    # Word count check
    if word_count < 300:
        issues.append("Content is too short (under 300 words)")
        score -= 20
    elif word_count < 600:
        issues.append("Content could be longer (under 600 words)")
        score -= 10
    
    # Heading structure
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if not headings:
        issues.append("No headings found in content")
        score -= 15
    else:
        h1_count = len(soup.find_all('h1'))
        if h1_count == 0:
            issues.append("No H1 heading found")
            score -= 10
        elif h1_count > 1:
            issues.append("Multiple H1 headings found (should have only one)")
            score -= 5
    
    # Keyword density in content
    content_lower = text.lower()
    if target_keywords:
        keyword_count = sum(1 for kw in target_keywords if kw.lower() in content_lower)
        keyword_ratio = keyword_count / len(target_keywords) if target_keywords else 0
        
        if keyword_ratio < 0.5:
            issues.append("Target keywords are not well represented in content")
            score -= 15
    
    # Paragraph length
    paragraphs = text.split('\n\n')
    long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]
    if long_paragraphs:
        issues.append(f"Found {len(long_paragraphs)} paragraphs that are too long (over 150 words)")
        score -= 5
    
    return {
        "score": max(0, score),
        "issues": issues,
        "word_count": word_count,
        "heading_count": len(headings)
    }

def generate_meta_title(title: str) -> str:
    """Generate an optimized meta title."""
    if len(title) <= 60:
        return title
    
    # Truncate intelligently
    words = title.split()
    result = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= 57:  # Leave room for "..."
            result.append(word)
            current_length += len(word) + 1
        else:
            break
    
    return ' '.join(result) + "..."

def generate_meta_description(content: str, target_keywords: List[str]) -> str:
    """Generate an optimized meta description."""
    # Convert markdown to text
    html_content = markdown.markdown(content)
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    # Get first few sentences
    sentences = re.split(r'[.!?]+', text)
    description = ""
    
    for sentence in sentences[:3]:
        if len(description) + len(sentence) < 150:
            description += sentence.strip() + ". "
        else:
            break
    
    description = description.strip()
    
    # If still too short, add keywords
    if len(description) < 120 and target_keywords:
        keywords_str = ", ".join(target_keywords[:3])
        if len(description) + len(keywords_str) + 2 < 160:
            description += f" {keywords_str}"
    
    # Truncate if too long
    if len(description) > 160:
        description = description[:157] + "..."
    
    return description

@router.post("/analyze", response_model=SEOAnalysisResponse)
async def analyze_seo(
    request: SEOAnalysisRequest,
    current_user = Depends(get_current_user)
):
    """Analyze blog post for SEO optimization."""
    
    # Analyze title
    title_analysis = analyze_title(request.title, request.target_keywords)
    
    # Analyze content
    content_analysis = analyze_content(request.content, request.target_keywords)
    
    # Calculate overall score
    overall_score = int((title_analysis["score"] + content_analysis["score"]) / 2)
    
    # Combine suggestions
    all_suggestions = title_analysis["issues"] + content_analysis["issues"]
    
    # Generate meta suggestions
    meta_title_suggestion = generate_meta_title(request.title)
    meta_description_suggestion = generate_meta_description(request.content, request.target_keywords)
    
    # Keyword analysis
    keyword_analysis = {
        "target_keywords": request.target_keywords,
        "title_keywords": title_analysis.get("keywords_found", []),
        "content_length": content_analysis.get("word_count", 0),
        "heading_count": content_analysis.get("heading_count", 0)
    }
    
    return SEOAnalysisResponse(
        score=overall_score,
        suggestions=all_suggestions,
        meta_title_suggestion=meta_title_suggestion,
        meta_description_suggestion=meta_description_suggestion,
        keyword_analysis=keyword_analysis
    )

@router.post("/generate-meta")
async def generate_meta_tags(
    title: str,
    content: str,
    target_keywords: List[str] = [],
    current_user = Depends(get_current_user)
):
    """Generate optimized meta tags for a blog post."""
    
    meta_title = generate_meta_title(title)
    meta_description = generate_meta_description(content, target_keywords)
    
    return {
        "meta_title": meta_title,
        "meta_description": meta_description,
        "title_length": len(meta_title),
        "description_length": len(meta_description)
    }
