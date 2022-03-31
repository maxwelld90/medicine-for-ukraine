import React from 'react'

import { container, prevButton, nextButton } from './styles'

export default function StepNavigation({
  prevButtonTitle = null,
  isPrevButtonEnabled = true,
  onClickPrev,

  nextButtonTitle,
  isNextButtonEnabled = true,
  onClickNext,
}) {
  return (
    <p style={container}>
      {prevButtonTitle && (
        <button
          style={prevButton}
          disabled={!isPrevButtonEnabled}
          onClick={onClickPrev}
        >
          {prevButtonTitle}
        </button>
      )}
      {nextButtonTitle && (
        <button
          style={nextButton}
          disabled={!isNextButtonEnabled}
          onClick={onClickNext}
        >
          {nextButtonTitle}
        </button>
      )}
    </p>
  )
}
