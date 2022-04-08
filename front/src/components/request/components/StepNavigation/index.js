import React from 'react'

// import { container, prevButton, nextButton } from './styles'
import classes from './StepNavigation.module.css';

export default function StepNavigation({
  prevButtonTitle = null,
  isPrevButtonEnabled = true,
  onClickPrev,

  nextButtonTitle,
  isNextButtonEnabled = true,
  onClickNext,
}) {
  return (
    <p className={classes.container}>
      {prevButtonTitle && (
        <button
          className={classes.prevButton}
          disabled={!isPrevButtonEnabled}
          onClick={onClickPrev}
        >
          {prevButtonTitle}
        </button>
      )}
      {nextButtonTitle && (
        <button
          className={classes.nextButton}
          disabled={!isNextButtonEnabled}
          onClick={onClickNext}
        >
          {nextButtonTitle}
        </button>
      )}
    </p>
  )
}
