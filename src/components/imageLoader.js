import React, { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function ImageLoader({ onUpload }) {
  const [t] = useTranslation(["translation", "common"]);
  const [files, setFiles] = useState([]);
  const fileRef = useRef();

  // Programmatically click the hidden file input element when the Button component is clicked
  const handleClick = () => {
    fileRef.current.click();
  };

  const onImageChange = (event) => {
    const newFiles = [...event.target.files].filter((f) => {
      return f.size / 1024 / 1024 <= 10; // less 10mb
    });
    setFiles([...files, ...newFiles]);
  };

  useEffect(() => {
    if (files.length > 0 && typeof onUpload === "function") {
      onUpload(files);
    }
  }, [files, onUpload]);

  const buttonLabel = files.length > 0 ? t("common:ADD_IMAGE") : t("common:UPLOAD_IMAGE");

  return (
    <div>
      <button onClick={handleClick}>{buttonLabel}</button>

      {files.map((file, i) => (
        <div className="screenshot-name" key={i}>
          {file.name}
        </div>
      ))}

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
