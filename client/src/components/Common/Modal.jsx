import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import './Modal.css';

const CLOSE_ANIMATION_MS = 180;

const Modal = ({ isOpen, onClose, children, contentClassName = '' }) => {
  const [isRendered, setIsRendered] = useState(isOpen);
  const [isClosing, setIsClosing] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsRendered(true);
      setIsClosing(false);
      return undefined;
    }

    if (!isRendered) {
      return undefined;
    }

    setIsClosing(true);
    const timeout = setTimeout(() => {
      setIsRendered(false);
      setIsClosing(false);
    }, CLOSE_ANIMATION_MS);

    return () => clearTimeout(timeout);
  }, [isOpen, isRendered]);

  useEffect(() => {
    if (!isRendered) {
      return undefined;
    }

    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);

    return () => {
      document.body.style.overflow = originalOverflow;
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isRendered, onClose]);

  if (!isRendered) {
    return null;
  }

  const stateClass = isClosing ? 'modal-state-closing' : 'modal-state-open';

  return createPortal(
    <div className={`app-modal-overlay ${stateClass}`} onClick={onClose}>
      <div
        className={`app-modal-content ${contentClassName} ${stateClass}`.trim()}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>,
    document.body
  );
};

export default Modal;
