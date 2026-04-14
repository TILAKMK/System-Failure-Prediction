'use client';

import { useState } from 'react';
import {
  Zap,
  BarChart3,
  Wind,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

type SidebarSection = 'electrical' | 'events' | 'environment';

interface SidebarProps {
  inputs: any;
  setInputs: (inputs: any) => void;
}

export default function Sidebar({ inputs, setInputs }: SidebarProps) {
  const [expandedSections, setExpandedSections] = useState({
    electrical: true,
    events: true,
    environment: true,
  });

  const toggleSection = (section: SidebarSection) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleChange = (key: string, value: number | string) => {
    setInputs({ ...inputs, [key]: value });
  };

  const TextInput = ({ label, value, onChange, step = 0.01 }: any) => (
    <div className="mb-4">
      <label className="block text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
        {label}
      </label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        step={step}
        className="w-full bg-slate-700 border border-cyan-500/50 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
      />
    </div>
  );

  const SelectInput = ({ label, value, onChange, options }: any) => (
    <div className="mb-4">
      <label className="block text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full bg-slate-700 border border-cyan-500/50 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-cyan-400"
      >
        {options.map((opt: any) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </div>
  );

  return (
    <div className="bg-gradient-to-b from-slate-800 to-slate-900 border border-cyan-500/20 rounded-lg p-6 space-y-4 sticky top-4">
      <h2 className="text-lg font-bold text-cyan-400">Dataset Source</h2>
      <div className="text-sm text-gray-400">
        <p>Using local dataset: CMOS_Battery_Failure_Dataset.csv</p>
      </div>

      <div className="border-t border-slate-600 pt-4">
        <h3 className="text-lg font-bold text-cyan-400 mb-4">⚙️ Manual Inputs</h3>

        {/* Electrical Health */}
        <div className="mb-3">
          <button
            onClick={() => toggleSection('electrical')}
            className="flex items-center justify-between w-full text-cyan-300 font-bold hover:text-cyan-200 transition"
          >
            <span className="flex items-center gap-2">
              <Zap size={16} />
              🔋 Electrical Health
            </span>
            {expandedSections.electrical ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {expandedSections.electrical && (
            <div className="mt-3 pl-4 space-y-3">
              <TextInput
                label="Battery Voltage"
                value={inputs.battery_voltage}
                onChange={(v: number) => handleChange('battery_voltage', v)}
                step={0.01}
              />
              <TextInput
                label="RTC Drift (sec/day)"
                value={inputs.rtc_drift}
                onChange={(v: number) => handleChange('rtc_drift', v)}
                step={1}
              />
            </div>
          )}
        </div>

        {/* System Events */}
        <div className="mb-3">
          <button
            onClick={() => toggleSection('events')}
            className="flex items-center justify-between w-full text-cyan-300 font-bold hover:text-cyan-200 transition"
          >
            <span className="flex items-center gap-2">
              <BarChart3 size={16} />
              📊 System Events
            </span>
            {expandedSections.events ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {expandedSections.events && (
            <div className="mt-3 pl-4 space-y-3">
              <TextInput
                label="Boot Errors"
                value={inputs.boot_errors}
                onChange={(v: number) => handleChange('boot_errors', v)}
                step={1}
              />
              <SelectInput
                label="CMOS Warning Flag"
                value={inputs.cmos_warning}
                onChange={(v: number) => handleChange('cmos_warning', v)}
                options={[0, 1]}
              />
              <SelectInput
                label="Reset BIOS Flag"
                value={inputs.reset_bios}
                onChange={(v: number) => handleChange('reset_bios', v)}
                options={[0, 1]}
              />
            </div>
          )}
        </div>

        {/* Environment */}
        <div className="mb-3">
          <button
            onClick={() => toggleSection('environment')}
            className="flex items-center justify-between w-full text-cyan-300 font-bold hover:text-cyan-200 transition"
          >
            <span className="flex items-center gap-2">
              <Wind size={16} />
              🌡️ Environment
            </span>
            {expandedSections.environment ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {expandedSections.environment && (
            <div className="mt-3 pl-4 space-y-3">
              <TextInput
                label="Power Cycle Count"
                value={inputs.power_cycle}
                onChange={(v: number) => handleChange('power_cycle', v)}
                step={1}
              />
              <TextInput
                label="System Age (years)"
                value={inputs.system_age}
                onChange={(v: number) => handleChange('system_age', v)}
                step={1}
              />
              <TextInput
                label="Ambient Temperature (°C)"
                value={inputs.temperature}
                onChange={(v: number) => handleChange('temperature', v)}
                step={0.1}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
