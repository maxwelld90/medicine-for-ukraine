import React, { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";

const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});

export default function ImageLoader({ onUpload, existingFiles }) {
  const [t] = useTranslation(["translation", "common"]);
  const [files, setFiles] = useState(existingFiles || []);
  const fileRef = useRef();

  // Programmatically click the hidden file input element when the Button component is clicked
  const handleClick = () => {
    fileRef.current.click();
  };

  const onImageChange = async (event) => {
    const newFiles = [...event.target.files].filter((f) => {
      return f.size / 1024 / 1024 <= 10; // less 10mb
    });

    const base64Files = await Promise.all(newFiles.map(async (file) => {
      file.base64 = await toBase64(file);
      return file;
    }));

    setFiles([...files, ...base64Files]);
  };

  const deleteItem = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
  }

  useEffect(() => {
    if (typeof onUpload === "function") {
      onUpload(files);
    }
  }, [files, onUpload]);

  const buttonLabel = files.length > 0 ? t("common:ADD_IMAGE") : t("common:UPLOAD_IMAGE");

  return (
    <div>
      <button onClick={handleClick}>{buttonLabel}</button>

      {files.length == 0 && 
      <span className="no-images">{t("common:STEP_FIVE.NO_SCREENSHOT")}</span>
      }

      {files.length > 0 &&
      <ul className="screenshots">
        {files.map((file, i) => (
          <li key={i}>
            <img src={file.base64} alt={file.name}/>
            <span className="screenshot-title">{file.name}</span>
            <div className="screenshot-remove-wrap">
              <span className="screenshot-remove" onClick={() => deleteItem(i)}>&#10006;</span>
            </div>
          </li>
        ))}
      </ul>}

      <input
        type="file"
        ref={fileRef}
        accept="image/*"
        onChange={onImageChange}
        style={{ display: "none" }}
      />
    </div>
  );
}
