import React from 'react';
import { Card, List, Tag, Typography } from 'antd';
import { RocketOutlined, ShieldOutlined, TeamOutlined } from '@ant-design/icons';

const { Text } = Typography;

interface Agent {
  id: string;
  name: string;
  team: 'red' | 'blue' | 'purple';
  description: string;
  status?: 'idle' | 'active' | 'error';
}

interface AgentStatusProps {
  agents?: Agent[];
}

const teamConfig = {
  red: { color: '#ff4d4f', icon: <RocketOutlined />, label: 'Red Team' },
  blue: { color: '#1890ff', icon: <ShieldOutlined />, label: 'Blue Team' },
  purple: { color: '#722ed1', icon: <TeamOutlined />, label: 'Purple Team' },
};

const statusColors = {
  idle: 'default',
  active: 'processing',
  error: 'error',
} as const;

const DEFAULT_AGENTS: Agent[] = [
  { id: 'recon', name: 'ReconAgent', team: 'red', description: 'Reconnaissance Specialist', status: 'idle' },
  { id: 'vuln_scanner', name: 'VulnScannerAgent', team: 'red', description: 'Vulnerability Assessment', status: 'idle' },
  { id: 'exploit_analyst', name: 'ExploitAnalystAgent', team: 'red', description: 'Exploit Analysis', status: 'idle' },
  { id: 'log_analyst', name: 'LogAnalystAgent', team: 'blue', description: 'Log Analysis', status: 'idle' },
  { id: 'incident_responder', name: 'IncidentResponderAgent', team: 'blue', description: 'Incident Response', status: 'idle' },
  { id: 'threat_hunter', name: 'ThreatHunterAgent', team: 'blue', description: 'Threat Hunting', status: 'idle' },
  { id: 'attack_surface', name: 'AttackSurfaceAgent', team: 'purple', description: 'Attack Surface Mapping', status: 'idle' },
  { id: 'report_generator', name: 'ReportGeneratorAgent', team: 'purple', description: 'Report Generation', status: 'idle' },
];

const AgentStatus: React.FC<AgentStatusProps> = ({ agents = DEFAULT_AGENTS }) => {
  return (
    <Card
      title="Security Agents"
      bordered={false}
      style={{ background: '#1a1a2e' }}
      styles={{ header: { color: '#fff', borderBottom: '1px solid #303050' } }}
    >
      <List
        dataSource={agents}
        renderItem={(agent) => {
          const team = teamConfig[agent.team];
          return (
            <List.Item style={{ borderBottom: '1px solid #303050', padding: '12px 0' }}>
              <List.Item.Meta
                avatar={<span style={{ color: team.color, fontSize: 20 }}>{team.icon}</span>}
                title={<Text style={{ color: '#fff' }}>{agent.name}</Text>}
                description={<Text style={{ color: '#888' }}>{agent.description}</Text>}
              />
              <div>
                <Tag color={team.color} style={{ marginRight: 8 }}>
                  {team.label}
                </Tag>
                <Tag color={statusColors[agent.status || 'idle']}>{(agent.status || 'idle').toUpperCase()}</Tag>
              </div>
            </List.Item>
          );
        }}
      />
    </Card>
  );
};

export default AgentStatus;
