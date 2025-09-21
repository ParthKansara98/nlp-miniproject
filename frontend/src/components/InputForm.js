import React, { useState } from 'react';
import { Link2, Type, Globe, FileText } from 'lucide-react';
import { isValidUrl, cleanUrl, containsGujarati } from '../utils/helpers';

const InputForm = ({ onSubmit, loading = false }) => {
  const [inputType, setInputType] = useState('url'); // 'url' or 'text'
  const [content, setContent] = useState('');
  const [options, setOptions] = useState({
    translate: true,
    summarize: true,
  });
  const [errors, setErrors] = useState({});

  const validateInput = () => {
    const newErrors = {};

    if (!content.trim()) {
      newErrors.content = inputType === 'url' ? 'Please enter a URL' : 'Please enter some text';
    } else if (inputType === 'url' && !isValidUrl(cleanUrl(content))) {
      newErrors.content = 'Please enter a valid URL';
    } else if (inputType === 'text' && content.length < 10) {
      newErrors.content = 'Please enter at least 10 characters';
    } else if (inputType === 'text' && !containsGujarati(content)) {
      newErrors.content = 'Text should contain Gujarati characters for translation';
    }

    if (!options.translate && !options.summarize) {
      newErrors.options = 'Please select at least one option (Translate or Summarize)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateInput()) {
      const processedContent = inputType === 'url' ? cleanUrl(content) : content;
      onSubmit({
        inputType,
        content: processedContent,
        ...options,
      });
    }
  };

  const handleInputTypeChange = (type) => {
    setInputType(type);
    setContent('');
    setErrors({});
  };

  const handleContentChange = (e) => {
    setContent(e.target.value);
    if (errors.content) {
      setErrors({ ...errors, content: null });
    }
  };

  const handleOptionChange = (option) => {
    const newOptions = { ...options, [option]: !options[option] };
    setOptions(newOptions);
    if (errors.options) {
      setErrors({ ...errors, options: null });
    }
  };

  const getPlaceholder = () => {
    if (inputType === 'url') {
      return 'Enter news article URL (e.g., https://example.com/news-article)';
    }
    return 'Enter Gujarati text to translate and summarize...';
  };

  const sampleUrls = [
    'https://divyabhaskar.co.in/gujarati-news',
    'https://gujaratsamachar.com/news',
    'https://sandesh.com/gujarati-news',
  ];

  const sampleText = 'આજે ગુજરાતમાં વરસાદ થવાની શક્યતા છે. હવામાન વિભાગે આગાહી કરી છે કે આગામી બે દિવસમાં મધ્યમ વરસાદ પડી શકે છે.';

  return (
    <div className="card max-w-4xl mx-auto">
      <div className="card-header">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary-600" />
          Process Gujarati Content
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          Translate and summarize Gujarati news articles
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Input Type Selection */}
        <div>
          <label className="label">Input Type</label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="inputType"
                value="url"
                checked={inputType === 'url'}
                onChange={() => handleInputTypeChange('url')}
                className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700 flex items-center gap-1">
                <Link2 className="w-4 h-4" />
                News URL
              </span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="inputType"
                value="text"
                checked={inputType === 'text'}
                onChange={() => handleInputTypeChange('text')}
                className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700 flex items-center gap-1">
                <Type className="w-4 h-4" />
                Direct Text
              </span>
            </label>
          </div>
        </div>

        {/* Content Input */}
        <div>
          <label className="label">
            {inputType === 'url' ? 'News Article URL' : 'Gujarati Text'}
          </label>
          {inputType === 'url' ? (
            <input
              type="text"
              value={content}
              onChange={handleContentChange}
              placeholder={getPlaceholder()}
              className={`input-field ${errors.content ? 'border-red-300' : ''}`}
              disabled={loading}
            />
          ) : (
            <textarea
              value={content}
              onChange={handleContentChange}
              placeholder={getPlaceholder()}
              rows={6}
              className={`textarea-field gujarati-text ${errors.content ? 'border-red-300' : ''}`}
              disabled={loading}
            />
          )}
          {errors.content && <p className="error-text">{errors.content}</p>}
          
          {/* Sample Data */}
          <div className="mt-2">
            <p className="text-xs text-gray-500 mb-1">
              {inputType === 'url' ? 'Sample URLs:' : 'Sample Text:'}
            </p>
            {inputType === 'url' ? (
              <div className="flex flex-wrap gap-2">
                {sampleUrls.map((url, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setContent(url)}
                    className="text-xs text-primary-600 hover:text-primary-800 underline"
                    disabled={loading}
                  >
                    {url.split('/')[2]}
                  </button>
                ))}
              </div>
            ) : (
              <button
                type="button"
                onClick={() => setContent(sampleText)}
                className="text-xs text-primary-600 hover:text-primary-800 underline gujarati-text"
                disabled={loading}
              >
                {sampleText.substring(0, 50)}...
              </button>
            )}
          </div>
        </div>

        {/* Processing Options */}
        <div>
          <label className="label">Processing Options</label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={options.translate}
                onChange={() => handleOptionChange('translate')}
                className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                disabled={loading}
              />
              <span className="ml-2 text-sm text-gray-700 flex items-center gap-1">
                <Globe className="w-4 h-4" />
                Translate to English
              </span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={options.summarize}
                onChange={() => handleOptionChange('summarize')}
                className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                disabled={loading}
              />
              <span className="ml-2 text-sm text-gray-700 flex items-center gap-1">
                <FileText className="w-4 h-4" />
                Generate Summary
              </span>
            </label>
          </div>
          {errors.options && <p className="error-text">{errors.options}</p>}
        </div>

        {/* Submit Button */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {content && (
              <span>
                {inputType === 'url' ? 'URL ready' : `${content.length} characters`}
              </span>
            )}
          </div>
          <button
            type="submit"
            disabled={loading || !content.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed min-w-[120px]"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="loading-spinner" />
                <span className="ml-2">Processing...</span>
              </div>
            ) : (
              <span>Process Content</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputForm;