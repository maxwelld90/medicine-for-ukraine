import React from 'react'
import { useTranslation } from 'react-i18next'

export default function Greeting({ onNext }) {
  const [t] = useTranslation(['translation', 'common'])

  return (
    <div>
      <h1>
        {t('common:REQUEST_GREETING.TITLE')}
      </h1>

      <p>{t('common:REQUEST_GREETING.FIRST_LINE')}</p>

      <p>{t('common:REQUEST_GREETING.SECOND_LINE')}</p>

      <p className="direction">
        <button onClick={onNext}>
          {t('common:REQUEST_GREETING.BUTTON')}
        </button>
      </p>
      
    </div>
  )
}
