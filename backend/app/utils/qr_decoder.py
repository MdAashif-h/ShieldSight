"""
QR Code Decoder Utility
Extracts URLs from QR code images
"""

import cv2
import numpy as np
from PIL import Image
from pyzbar import pyzbar
from typing import List, Dict, Optional, Tuple
import logging
import base64
import io
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class QRDecoder:
    """Decode QR codes from images and extract URLs"""
    
    SHORTENER_DOMAINS = {
        'qrco.de', 'bit.ly', 'tinyurl.com', 't.co',
        'goo.gl', 'is.gd', 'cutt.ly', 'rebrand.ly',
        'ow.ly', 'buff.ly', 'adf.ly', 'bc.vc',
        'tiny.cc', 'lc.chat', 'rb.gy'
    }
    
    @staticmethod
    def is_shortened_url(url: str) -> bool:
        """Check if URL uses a shortener service"""
        try:
            domain = urlparse(url).netloc.lower().replace('www.', '')
            return any(domain.endswith(shortener) or domain == shortener 
                      for shortener in QRDecoder.SHORTENER_DOMAINS)
        except Exception:
            return False
    
    @staticmethod
    def expand_url(url: str, timeout: int = 5) -> Tuple[str, List[str]]:
        """
        Expand shortened URL to final destination
        
        Returns:
            (final_url, redirect_chain)
        """
        try:
            response = requests.head(
                url,
                allow_redirects=True,
                timeout=timeout,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            # Build redirect chain
            redirect_chain = []
            if hasattr(response, 'history') and response.history:
                redirect_chain = [r.url for r in response.history]
            
            final_url = response.url if response.url else url
            return final_url, redirect_chain
            
        except Exception as e:
            logger.warning(f"URL expansion failed for {url}: {e}")
            return url, []
    
    @staticmethod
    def _calculate_quality(obj) -> str:
        """
        Calculate QR code quality based on size and detectability
        pyzbar doesn't consistently expose .quality attribute
        """
        try:
            # Try to use quality if available
            if hasattr(obj, 'quality') and obj.quality is not None:
                if obj.quality > 50:
                    return 'high'
                elif obj.quality > 20:
                    return 'medium'
                else:
                    return 'low'
        except:
            pass
        
        # Fallback: use size as quality indicator
        size = obj.rect.width * obj.rect.height
        if size > 10000:  # Large QR = high quality
            return 'high'
        elif size > 3000:
            return 'medium'
        else:
            return 'low'
    
    @staticmethod
    def decode_from_base64(base64_image: str) -> List[Dict]:
        """
        Decode QR codes from base64 image string
        
        Args:
            base64_image: Base64 encoded image (with or without prefix)
            
        Returns:
            List of decoded QR codes with URLs and metadata
        """
        try:
            # Remove data URL prefix if present
            if 'base64,' in base64_image:
                base64_image = base64_image.split('base64,')[1]
            
            # Decode base64 to image
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = img_array
            
            # Decode QR codes
            decoded_objects = pyzbar.decode(img_gray)
            
            results = []
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                
                # Check if it's a URL
                if data.startswith(('http://', 'https://', 'www.')):
                    results.append({
                        'data': data,
                        'type': obj.type,
                        'quality': QRDecoder._calculate_quality(obj),
                        'rect': {
                            'x': obj.rect.left,
                            'y': obj.rect.top,
                            'width': obj.rect.width,
                            'height': obj.rect.height
                        }
                    })
                else:
                    logger.warning(f"QR code contains non-URL data: {data[:50]}")
            
            if not results:
                logger.warning("No URLs found in QR code(s)")
                
            return results
            
        except Exception as e:
            logger.error(f"QR decoding error: {str(e)}")
            raise ValueError(f"Failed to decode QR code: {str(e)}")
    
    @staticmethod
    def validate_qr_image(image_data: bytes) -> bool:
        """Validate if image is valid and contains QR code"""
        try:
            image = Image.open(io.BytesIO(image_data))
            # Check size
            if image.size[0] < 50 or image.size[1] < 50:
                return False
            # Check format
            if image.format not in ['PNG', 'JPEG', 'JPG', 'WEBP']:
                return False
            return True
        except Exception:
            return False