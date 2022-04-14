import React, { useContext, useState } from 'react'
import { useAsync } from 'react-use'
import { useTranslation } from 'react-i18next'

import { fetchAddress } from '../../api'
import Content from '../Content'

import ImageLoader from '../imageLoader'
import { RequestContext } from './requestContext'
import StepDescription from './components/StepDescription'
import StepNavigation from './components/StepNavigation'

import { getStaticPath } from '../../helpers'

import classes from './request.module.css'

// Check if each store has at least one file
const isValidRequest = (request) =>
  Object.values(request.stores).every((s) => s.screenshots && s.screenshots.length > 0)

export default function Confirmation({ onNext }) {
  const [request] = useContext(RequestContext)
  const [isCompletedStep, setIsCompletedStep] = useState(false)
  const [t] = useTranslation(['translation', 'common'])

  const { loading, error, value } = useAsync(() => fetchAddress(request.recipientId))

  const getOnUploadHandler = (index) => (files) => {
    request.stores[index].screenshots = files
    setIsCompletedStep(isValidRequest(request))
  }

  return (
    <Content error={error} loading={loading}>
      {() => (
        <div>
          <StepDescription
            step="5/5"
            title={t('common:STEP_FIVE.TITLE')}
            firstLine={t('common:STEP_FIVE.FIRST_LINE')}
          />

          <div className={classes.addressContainer}>
            <div className={classes.addressText}>{value.warehouse_address.address}</div>
            <img className={classes.postMark} style={{ width: '70px' }} src={getStaticPath('/img/postmark.svg')} alt="postmark" />
          </div>

          <h2>Upload Screenshot(s)</h2>

          <p>{t('common:STEP_FIVE.SECOND_LINE')}</p>

          <ul className={classes.fileList}>
            {Object.entries(request.stores).map(([i, store]) => (
              <li key={i} className={classes.listElement}>
                <span>{store.store_domain}</span>
                <ImageLoader onUpload={getOnUploadHandler(i)} existingFiles={store.screenshots} />
              </li>
            ))}
          </ul>

          <StepNavigation
            nextButtonTitle={t('common:FINAL_BUTTON')}
            isNextButtonEnabled={isCompletedStep}
            onClickNext={onNext}
          />
        </div>
      )}
    </Content>
  )
}
